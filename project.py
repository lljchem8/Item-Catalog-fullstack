#!/usr/bin/env python3

from flask import Flask


app = Flask(__name__)


@app.route('/')
@app.route('/catalog')
def showCatalog():
    return "show all kinds of catalog"


@app.route('/catalog/<string:name>')
@app.route('/catalog/<string:name>/items')
def showCatalogName(name):
    return "catalog {}".format(name)


@app.route('/catalog/<string:catName>/<string:itemName>')
def showitemName(catName, itemName):
    return "catname {}, itemName {}".format(catName, itemName)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
