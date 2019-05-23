#!/usr/bin/env python3

from flask import Flask


app = Flask(__name__)


@app.route('/')
@app.route('/catalog')
def shwoCatalog():
    return "show all kinds of catalog"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
