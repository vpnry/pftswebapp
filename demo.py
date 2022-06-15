import os
from pftswebapp import web_fts, send_from_directory

# document_root should not be named as 'static'
doc_root = 'documents'
app = web_fts(doc_root)

cwd = os.path.join(os.path.abspath(os.path.dirname(__file__)), doc_root)

# serve static files in doc_root


@app.route(f'/{doc_root}/<path:request_pat>', methods=['POST', 'GET'])
def serve_static(request_pat):
    print('Requesting:', request_pat)

    # use cwd; relative path doc_root will yeild not found errors
    return send_from_directory(cwd, request_pat)


# app.run(debug=True) runs slower
app.run(debug=False)
