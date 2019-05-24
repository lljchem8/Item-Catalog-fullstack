#!/usr/bin/env python3

from flask import Flask, request


app = Flask(__name__)


@app.route('/')
@app.route('/catalog')
def showCatalog():
    return "show all kinds of catalog"

# show all catalog


@app.route('/catalog/<string:name>')
@app.route('/catalog/<string:name>/items')
def showCatalogName(name):
    return "catalog {}".format(name)

# add a new catalog


@app.route('/catalog/new', methods=['GET', 'POST'])
def newCatalog():
    if (request.method == 'POST'):
        return "a new catalog added"
    else:
        return "its not a valid post request"


# delete a catalog
@app.route('/catalog/<string:name>/delete', methods=['GET', 'POST'])
def deleteCatalog(name):
    if (request.method == 'POST'):
        return "a catalog is deleted"
    else:
        return "not a valid post request"

# edit a catalog


@app.route('/catalog/<string:name>/edit', methods=['GET', 'POST'])
def editCatalog(name):
    if (request.method == 'POST'):
        return "the catalog has been edited"
    else:
        return "not a valid request"


@app.route('/catalog/<string:catName>/<string:itemName>')
def showitemName(catName, itemName):
    return "catname {}, itemName {}".format(catName, itemName)

# create a new item


@app.route('/catalog/<string:catName>/new', methods=['GET', 'POST'])
def newItem(catName):
    if (request.method == 'POST'):
        return "added a new item"
    else:
        return "not a valid post"

# edit an item


@app.route('/catalog/<string:catName>/<string:itemName>/edit', methods=['GET', 'POST'])
def editItem(catName, itemName):
    if (request.method == 'POST'):
        return "the item has been edited"
    else:
        return "not a valid post"

# delete an item


@app.route('/catalog/<string:catName>/<string:itemName>/delete', methods=['GET', 'POST'])
def deleteItem(catName, itemName):
    if (request.method == 'POST'):
        return "the item has been deleted"
    else:
        return "not a valid post"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
