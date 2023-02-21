'''Quick & Simple FTS Web App

 * Automatically detect & index new folders, and build web UI
 * Note: This app is not intended to meet security or performance
 * requirements for an online production server.
 * It was initially written to be used on Termux app on my Android phone.
 * https://github.com/vpnry/pftswebapp

'''

import os
import random

from flask import Flask, render_template, request, send_from_directory


from .checker import check_init_db, check_init_somedirs_db
from .searcher import search_this

# import os.path as Path
# index_html = Path.join(
#     Path.abspath(
#         Path.dirname(__file__)),
#     'templates',
#     'index.html')

intNum = random.randrange(1 << 38, 1 << 39)


def web_fts(document_root='documents', filter_dir_list=None,
            db_dir_path='indexed_database'):

    app = Flask(__name__)
    print(' ** pftswebapp module path', app.root_path)
    app.config['SECRET_KEY'] = f'change_this_super_secret_key_{intNum}'

    SEARCH_OPS = {'distance': '', 'exact': '', 'prefix': ''}
    ORDER_OPS = {'path': '', 'rank': '', 'bm25': ''}

    DB_DICT = {}
    if isinstance(document_root, str):
        document_root = document_root.strip()
    if document_root[-1:] == os.sep:
        document_root = document_root[0:-1]

    if isinstance(filter_dir_list, list):
        DB_DICT = check_init_somedirs_db(
            document_root, db_dir_path, filter_dir_list)
    else:
        DB_DICT = check_init_db(document_root, db_dir_path)

    @app.route('/', methods=['POST', 'GET'])
    def index():
        if request.method == 'POST':
            db_name = request.form['database']

            keyword = request.form['keyword']
            db_path = DB_DICT['dbpath'][db_name]
            search_mode = request.form['searchmode']
            distance_value = request.form['distancevalue']
            extract_len = request.form['extractlen']
            hit_limit = request.form['hitlimit']
            order_by = request.form['orderby']

            # TODO: handle these forms with Flask-WTF? instead
            all_db = DB_DICT['dbname'].copy()
            all_db[db_name] = 'checked'

            all_smodes = SEARCH_OPS.copy()
            all_smodes[search_mode] = 'checked'

            all_orders = ORDER_OPS.copy()
            all_orders[order_by] = 'checked'

            search_res = search_this(
                keyword=keyword,
                db_path=db_path,
                search_mode=search_mode,
                distance_value=distance_value,
                extract_len=extract_len,
                hit_limit=hit_limit,
                order_by=order_by)

            return render_template(
                'index.html',
                document_root=document_root,
                keyword=keyword,
                all_db=all_db,
                search_res=search_res,
                all_orders=all_orders,
                extract_len=extract_len,
                hit_limit=hit_limit,
                all_smodes=all_smodes,
                distance_value=distance_value)
        else:
            all_db = DB_DICT['dbname'].copy()
            if all_db:
                all_db[list(all_db.keys())[0]] = 'checked'

            all_smodes = SEARCH_OPS.copy()
            if all_smodes:
                all_smodes['distance'] = 'checked'

            all_orders = ORDER_OPS.copy()
            if all_orders:
                all_orders['rank'] = 'checked'

            return render_template(
                'index.html',
                all_db=all_db,
                document_root=document_root,
                all_smodes=all_smodes,
                all_orders=all_orders
            )

    # @app.route(f'/{document_root}/<path:request_pat>', methods=['POST', 'GET'])
    # def serve_static(request_pat):
    #     '''Serve static document (.html etc...)'''
    #     print('Requesting:', request_pat)
    #     return send_from_directory(f'{document_root}', request_pat)

    @app.template_filter('stripsqlite3')
    def stripsqlite(s):
        '''A custom filter func to shorten db names in the web UI'''
        s = s.strip()
        if s[-8:] == '.sqlite3':
            return s[0:-8]
        return s
    return app
