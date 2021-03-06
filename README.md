## Introduction

+ This is a simple Pythonic full text search (fts) web app, powered by `Sqlite3 FTS5`, that can be run on Termux app (Android OS).

+ Its indexed database files are compatible with this [PHP fts app](https://github.com/vpnry/fts).

+ Caveats: This quick implement web app is **NOT INTENDED** to meet security or performance requirements for an online production server. Read other bonus  [limitations](#limitation).

![](./pftswebapp.jpg)


## Installation

Your device may need an active Internet connection to download these Python dependencies `flask` and `lxml`, `beautifulsoup4` during the installation.

Method 1

```
python3 -m pip install git+https://github.com/vpnry/pftswebapp.git#egg=pftswebapp

```

Method 2

Or download this file [dist/pftswebapp-0.0.1.tar.gz](dist/pftswebapp-0.0.1.tar.gz), then `cd` to its dir and run:

```python 

python3 -m pip install ./pftswebapp-0.0.1.tar.gz

```

For Unix family platforms, it should work. Not sure whether it can be run on Window.

## Usage

+ Consider this localhost directory tree:

```text

localhost
├── this_file_will_not_be_indexed.txt
├── website_1
│   ├── file.html
│   └── file.txt
└── website_2
    ├── file.html
    ├── file.txt
    └── sub_dir
        ├── file.html
        └── file.txt
```

+ Create an `app.py` file with this snippet: 

```python

import os
from pftswebapp import web_fts, send_from_directory

# document_root should not be named as 'static'

document_root = 'localhost'
app = web_fts(document_root)


cwd = os.path.join(os.path.abspath(os.path.dirname(__file__)), document_root)

# serve static files in document_root


@app.route(f'/{document_root}/<path:request_pat>', methods=['POST', 'GET'])
def serve_static(request_pat):
    print('Requesting:', request_pat)

    # use cwd; relative path document_root will yeild not found errors
    return send_from_directory(cwd, request_pat)

# app.run(debug=True) runs slower
app.run(debug=False)


```

+ Then run: `python3 app.py`. It will ignore all of the first level files `localhost/file.*`, and only index directories `localhost/dirname`. So, here, it will recursively index `website_1` and `website_2` and save them as `website_1.sqlite3`, `website_1.sqlite3` to the `indexed_database` dir. 


+ Open the address it shown in the terminal, for example `http://127.0.0.1:5000/`, with a standard browser.

+ To stop the app press `Ctrl + C`.

+ To index a few selected dirs only, see [demo_selected_dir](demo_selected_dir.py).


## Tips
 
+ On computer there are many good fts desktop apps with many more features. Use them instead.

### On Android

Install Termux, and Termux Widget app (get them from F-droid store for newer versions). Use Termux Widget to place a shortcut on the phone home screen.

In Termux, create `~/.shortcuts/pyfts.sh` file with this snippet:

```bash 

# ~/.shortcuts/pyfts.sh

echo "Starting Python FTS"
cd /storage/emulated/0/python_fts/

termux-open http://127.0.0.1:5000

python3 app.py 


```

Then `chmod +777 ~/.shortcuts/pyfts.sh`

+ `/storage/emulated/0/python_fts/` is the place where we created `app.py`.

+ On the phone home screen, click on the Termux widget `pyfts`. Since the shortcut openned the web address before the server started, you need to refresh the web browser.


### On iOS/iPadOS

Use **phpwin** app to run this [PHP fts app](https://github.com/vpnry/fts) which is faster and more convenient. The indexed database files of this web app are compatible with it.

May also try this web app in **iSH** app.

Use Apple Shortcuts app to make a shortcut on the home screen.

## Limitation

+ Again! This offline & quick implement web app is **NOT INTENDED** to meet security or performance requirements for an online production server.

+ It recognises new dirs only, not new additional files you add to the indexed dirs. To re-index the directories, delete the old indexed `.sqlite3` and restart the app.

+ Currently, it only handles `.txt, .html, .htm` files. (You may use **Apache Tika**, etc... to convert other file formats to text `.txt` or `.html` first. Or modify `indexer.py` to handle more file formats.)


## Attributions

+ Ref: `https://stackoverflow.com/a/3861725`


+ Realistic iOS Switch In Pure CSS

```css 
/**
 * Realistic iOS Switch In Pure CSS
 * is adapted from
 * Link: https://www.cssscript.com/realistic-ios-switch-pure-css/
 * Author: Pontus Nilsson
 * License: MIT
 */
```

