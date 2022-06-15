'''Prepare text and perform sqlite3 fts5 indexing

+ Support: indexing .html .htm and .txt only.
+ If there are other file types like .pdf, .docx...,
may use Apache Tika to convert them into .txt or .html first.
'''

import re
import sqlite3
import os
import glob
from pathlib import PurePath
from bs4 import BeautifulSoup

from .util import Util


def _unzip_rename(zip_file):
    bare_name = zip_file[0: -len('.zip')]
    no_ver_name = re.sub(r'[\d\W]+', '', bare_name)

    cm_unzip = f'unzip -o -qq {zip_file}'
    cm_cpbackup = f'cp -r {bare_name} {bare_name}_origin'
    cm_rename = f'mv -f {bare_name} {no_ver_name}'

    os.system(cm_unzip)
    os.system(cm_cpbackup)
    os.system(cm_rename)

    return no_ver_name


def html_to_text(html):
    # use lxml parser
    m = BeautifulSoup(html, 'lxml')
    return m.get_text()


def split_token(content, token):
    # ref: https://stackoverflow.com/a/3861725
    res = ''
    words = content.split()
    for i in range(0, len(words), token):
        res += ' '.join(words[i:i + token]) + '\n'
    return res


def prepare_line_chunk(content, token=800):
    content = content.splitlines()
    lines = [line.strip() for line in content if line.strip()]

    content = "\n".join(lines)
    content = re.sub(r"(\S)[ \t]*(?:\r\n|\n)[ \t]*(\S)", r"\1 \2", content)
    content = re.sub(r"[\s]+", r" ", content)
    content = re.sub(r"\n", " ", content)

    return split_token(content, token)


def index_dir_fts(in_dir, db=None, allow_ext='html,htm,txt'):
    '''
    Do not use the whole file content as a single string for indexing
    Because:
    1- fts5 snippet function will only see it as 1 fragment and
    2- the fts5 SORT BY path function will be much slower
    '''

    skipped_index_log = ''

    print(f' * Listing files in:', in_dir)

    ext_list = Util.create_ext_list(allow_ext)
    files = Util.scandir_file(in_dir, '*', recursive=True)

    if not files:
        print(f' * Not found any files to index', in_dir)
        return

    len_file = len(files)
    print_chunk = 1 + (len_file // 100)

    print(' * Found total', len_file, 'files')
    print(
        ' * Will index',
        ext_list,
        'files only. Indexing may take time please wait...')

    if not db:
        no_ver_name = re.sub(r'[\d\W]+', '', in_dir)
        db = f'{no_ver_name}.sqlite3'
    if os.path.isfile(db):
        os.remove(db)

    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("CREATE VIRTUAL TABLE pn USING fts5(path, cont)")

    n = 0
    f = ''
    for f in files:
        text = ''
        # handle txt, html, htm only
        if f.endswith('.txt'):
            text = Util.read_file(f)
        elif f.endswith(tuple(['.html', '.htm'])):
            text = html_to_text(Util.read_file(f))
        else:
            skipped_index_log += f'Skipped file ext: ' + f + '\n'
            continue
        text = text.strip()
        if len(text) < 1:
            skipped_index_log += f' ** No text: {f}\n'
            continue

        # chunk text and index
        text = prepare_line_chunk(text).splitlines()

        doc_root = PurePath(in_dir).parts[0]
        pat_file = f[len(doc_root + str(os.sep)):]
        tuble_list = [(pat_file, t.strip())
                      for t in text if len(t.strip()) > 3]

        c.executemany("INSERT INTO pn VALUES (?,?)", tuble_list)
        n += 1
        if n % print_chunk == 0:
            print(str(n) + ". Indexed: " + f)
    print(" * " + str(n) + ". The last file: " + f)

    print(" * Optimizing the database...")
    c.execute("INSERT INTO pn(pn) VALUES('optimize')")
    conn.commit()
    conn.close()

    print(' * Done indexed:', n, '/', len_file)

    log_filename = f'{Util.get_filename(db)}_index_log.txt'
    if n < len_file:
        print('Not all files are indexed.\nCheck the log file:', log_filename)

    if skipped_index_log:
        allow_ext_add = 'Note: allowed ext in indexer.py: ' + \
            ', '.join(ext_list) + '\n-------------------\n'
        skipped_index_log = allow_ext_add + skipped_index_log

        Util.write_file(log_filename, skipped_index_log)
        print(f' ** Check index log files: {log_filename}')
