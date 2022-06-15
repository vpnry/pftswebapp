import os
from pathlib import PurePath

from .indexer import index_dir_fts
from .util import Util


def run_index_dir(doc_root_path, db_path):
    sqlite_filename = Util.get_shortname(doc_root_path)
    db_path = os.path.join(db_path, f'{sqlite_filename}.sqlite3')

    index_dir_fts(doc_root_path, db_path, allow_ext='html,htm,txt')
    print(f' * Indexed & saved to {db_path}\n')


def check_doc_vs_db(doc_root_path, db_path):
    '''check new directories located in @doc_root_path

    if they haven't been indexed, start indexing, and save to @db_path
    '''

    Util.mkdir_res(doc_root_path)
    Util.mkdir_res(db_path)

    dir_paths = Util.scandir_dir(doc_root_path, recursive=False)

    if not dir_paths:
        return []
    dir_names_only = [Util.get_shortname(dir_pat) for dir_pat in dir_paths]
    sqlite3_file_paths = Util.scandir_file(db_path, 'sqlite3', recursive=True)

    sqlite_filenames = [Util.get_filename(
        file_path) for file_path in sqlite3_file_paths]

    for n in range(len(dir_names_only)):
        if f'{dir_names_only[n]}.sqlite3' not in sqlite_filenames:
            print(f' ** Found a new folder: {dir_paths[n]}, start indexing')
            run_index_dir(dir_paths[n], db_path)


def check_init_db(doc_root_path, db_path):
    check_doc_vs_db(doc_root_path, db_path)
    full_path_dict = {}
    db_name_dict = {}
    db_list = Util.scandir_file(db_path, 'sqlite3', recursive=True)
    if not db_list:
        print(' * No sqlite3 files found. Generating dummy database...')
        Util.create_dummy_text(doc_root_path)
        # index dummy text
        check_doc_vs_db(doc_root_path, db_path)
        db_list = Util.scandir_file(db_path, 'sqlite3', recursive=True)

    print(
        f'\n * Found total {len(db_list)} sqlite3 files:\n',
        db_list,
        '\n -----\n')

    for file_path in sorted(db_list):
        name = Util.get_filename(file_path)
        full_path_dict[name] = file_path
        db_name_dict[name] = ''

    '''
        the below dicts will be used to keep the checked checkboxes checked
        TODO: use Flask-WTF etc to handle them instead
    '''

    return {'dbpath': full_path_dict, 'dbname': db_name_dict}


# index a selected dir path list only
def check_somedirs_vs_db(doc_root_path, db_path, filter_dir_list=None):
    '''check new directories located in @dirpath_list

    if they haven't been indexed, start indexing, and save to @db_path
    '''

    Util.mkdir_res(db_path)
    dir_paths = Util.scandir_dir(doc_root_path, recursive=False)

    if filter_dir_list and isinstance(filter_dir_list, list):

        # print('All dirs in doc_root', dir_paths)
        dir_paths = [
            d for d in dir_paths if d.startswith(
                tuple(filter_dir_list))]
        print('\n * Selected dir list:', dir_paths)

    if not dir_paths or not isinstance(dir_paths, list):
        return []
    dir_names_only = [Util.get_shortname(dir_pat) for dir_pat in dir_paths]
    sqlite3_file_paths = Util.scandir_file(db_path, 'sqlite3', recursive=True)

    sqlite_filenames = [Util.get_filename(
        file_path) for file_path in sqlite3_file_paths]

    for n in range(len(dir_names_only)):
        if f'{dir_names_only[n]}.sqlite3' not in sqlite_filenames:
            print(f'\n ** Found a new folder: {dir_paths[n]}, start indexing')
            run_index_dir(dir_paths[n], db_path)


def check_init_somedirs_db(dirpath_list, db_path, filter_dir_list=None):
    check_somedirs_vs_db(dirpath_list, db_path, filter_dir_list)
    full_path_dict = {}
    db_name_dict = {}
    db_list = Util.scandir_file(db_path, 'sqlite3', recursive=True)
    if not db_list:
        print(' * No sqlite3 files found. Stop')
        return
        Util.create_dummy_text(dirpath_list)
        # index dummy text
        check_doc_vs_db(dirpath_list, db_path)
        db_list = Util.scandir_file(db_path, 'sqlite3', recursive=True)

    print(
        f'\n * Found total {len(db_list)} sqlite3 files:\n',
        db_list,
        '\n -----\n')

    for file_path in sorted(db_list):
        name = Util.get_filename(file_path)
        full_path_dict[name] = file_path
        db_name_dict[name] = ''

    '''
        the below dicts will be used to keep the checked checkboxes checked
        TODO: use Flask-WTF etc to handle them instead
    '''

    return {'dbpath': full_path_dict, 'dbname': db_name_dict}
