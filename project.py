#!/usr/bin/env python3

from flask import Flask, request, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Catalog, Item, Base

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

# show all catalog


@app.route('/')
@app.route('/catalog')
def showCatalog():
    catalogs = session.query(Catalog).all()
    items = session.query(Item.itemName, Catalog.catalogName).filter(
        Item.catalog_id == Catalog.id).order_by(Item.id.desc()).limit(3)

    return render_template("catalog.html", catalogs=catalogs, items=items)

# show all items for a specific catalog


@app.route('/catalog/<string:name>')
@app.route('/catalog/<string:name>/items')
def showCatalogItems(name):
    catalogs = session.query(Catalog).all()
    catalog = session.query(Catalog).filter_by(
        catalogName=name.replace('-', ' ')).one()
    items = session.query(Item).filter_by(catalog_id=catalog.id).all()
    return render_template("items.html", catalogs=catalogs, items=items, selected_catalog=catalog)


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


# show an item
@app.route('/catalog/<string:catalogName>/<string:itemName>')
def showItemName(catalogName, itemName):
    item = session.query(Item).filter_by(itemName=itemName).one()
    catalog = session.query(Catalog).filter_by(
        catalogName=catalogName.replace('-', ' ')).one()
    return render_template('item.html', catalogName=catalog.catalogName, item=item)

# create a new item


@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    if (request.method == 'POST'):
        return render_template('newItem.html')
    else:
        return render_template('newItem.html')

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
