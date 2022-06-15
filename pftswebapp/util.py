import re
import os
import glob
import sqlite3
from pathlib import PurePath


class Util():
    def mkdir_res(d=None):
        if d:
            os.makedirs(d, exist_ok=True)
        return True

    def get_fileext_with_dot(file_path):
        ext_dot = PurePath(file_path).suffix
        return ext_dot

    def get_filename(file_path):
        name_parts = PurePath(file_path).parts
        return name_parts[-1]

    def get_shortname(file_path):
        name = Util.get_filename(file_path)
        non_word = re.compile(r'\W*', re.IGNORECASE)
        return re.sub(non_word, '', name)

    def read_file(f, encoding='utf-8'):
        try:
            with open(f, 'r', encoding=encoding) as fi:
                return fi.read()
        except Exception as e:
            with open(f, 'rb') as fii:
                print(
                    f'''Error while reading file with {encoding},
                    switched to "rb" mode.''')
                return fii.read()

    def write_file(f, data, encoding='utf-8'):
        with open(f, 'w', encoding=encoding) as fo:
            try:
                fo.write(data)
                print(f' * Wrote {f} with {encoding}')
                return True
            except Exception as e:
                print(f' * Errors occured when writing {f}', e)
                raise e

    def glob_files(d, ext="*", recursive=True):
        ext = '.' + ext.strip().strip('.')
        pattern = os.path.join(d, '**', f'*{ext}')
        li = glob.glob(pattern, recursive=recursive)
        return [f for f in li if os.path.isfile(f)]

    def glob_dirs_only(d, recursive=False):
        pattern = os.path.join(d, '*')
        li = glob.glob(pattern, recursive=recursive)
        return [d for d in li if os.path.isdir(d)]

    def scandir_dir(d, recursive=False):
        res = []
        with os.scandir(d) as di:
            for e in di:
                if e.is_dir():
                    if recursive:
                        res.extend(Util.scandir_dir(e, recursive=recursive))
                    else:
                        res.append(e.path)
        return res

    def strip_add_dot(t):
        return '.' + t.strip().strip('.')

    def create_ext_list(ext):
        res = []
        if isinstance(ext, str):
            if Util.strip_add_dot(ext) == '.*':
                return ['.*']
            else:
                res = ext.split(',')
        elif isinstance(ext, list):
            res = ext
        res = [Util.strip_add_dot(e) for e in res if Util.strip_add_dot(e)]
        return res

    def scandir_file(d, ext='*', recursive=False):
        '''
        ext: str 'html,htm,txt' or list ['html', 'htm', 'txt]
        ext: '*' all
        '''
        res = []
        ext_list_with_dot = Util.create_ext_list(ext)
        with os.scandir(d) as di:
            for e in di:
                if e.is_file():
                    res.append(e.path)
                elif e.is_dir() and recursive:
                    res.extend(
                        Util.scandir_file(
                            e, ext_list_with_dot, recursive=recursive))

        if '.*' in ext_list_with_dot:
            return res
        else:
            return [e for e in res if e.endswith(tuple(ext_list_with_dot))]

    def create_dummy_text(documents_path):
        example_dirs = [
            'website_1',
            'website_2',
            os.path.join('website_2', 'sub_dir')
        ]
        for example in example_dirs:
            dummy_db_dir = os.path.join(documents_path, example)
            Util.mkdir_res(dummy_db_dir)

            text = 'This is an example text file.'
            html = '<p>This <b>is</b> an example html file.</p>'

            Util.write_file(os.path.join(dummy_db_dir, 'file1.txt'), text)
            Util.write_file(os.path.join(dummy_db_dir, 'file2.html'), html)
