import os
from pftswebapp import web_fts, send_from_directory


'''An example localhost directory tree

localhost
├── this_file_will_not_be_indexed.txt
├── website1
│   ├── file.html
│   └── file.txt
└── website2
    ├── file.html
    ├── file.txt
    └── sub_dir
        ├── file.html
        └── file.txt
'''
# document_root should not be named as 'static'
doc_root = 'localhost'

selected_dir = ['localhost/website2']


# this will only index website2
app = web_fts(doc_root, filter_dir_list=selected_dir)

cwd = os.path.join(os.path.abspath(os.path.dirname(__file__)), doc_root)

# serve static files in doc_root


@app.route(f'/{doc_root}/<path:request_pat>', methods=['POST', 'GET'])
def serve_static(request_pat):
    print('Requesting:', request_pat)

    # use cwd; relative path doc_root will yeild not found errors
    return send_from_directory(cwd, request_pat)


# app.run(debug=True) runs slower
app.run(debug=False)
