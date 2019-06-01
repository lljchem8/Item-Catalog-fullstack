#!/usr/bin/env python3

from flask import Flask, request, render_template, make_response, jsonify, redirect, url_for

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


# show an item
@app.route('/catalog/<string:catalogName>/<string:itemName>')
def showItemName(catalogName, itemName):
    item = session.query(Item).filter_by(itemName=itemName).one()
    catalog = session.query(Catalog).filter_by(
        catalogName=catalogName.replace('-', ' ')).one()
    return render_template('item.html', item=item, catalog=catalog)

# create a new item


@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():

    if (request.method == 'POST'):
        catalog = session.query(Catalog).filter_by(
            catalogName=request.form['catalogname']).one()
        newItem = Item(itemName=request.form['coinname'], description=request.form['description'],
                       catalog_id=catalog.id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showCatalog'))

    else:
        catalogs = session.query(Catalog).all()
        return render_template('newItem.html', catalogs=catalogs)

# edit an item


@app.route('/catalog/<string:catalogName>/<string:itemName>/edit', methods=['GET', 'POST'])
def editItem(catalogName, itemName):
    item = session.query(Item).filter_by(itemName=itemName).one()
    selectedCatalog = session.query(Catalog).filter_by(
        catalogName=catalogName).one()
    catalogs = session.query(Catalog).all()
    if (request.method == 'POST'):
        if (request.form['coinname']):
            item.itemName = request.form['coinname']
        if (request.form['description']):
            item.description = request.form['description']
        session.add(item)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('editItem.html', item=item, selectedCatalog=selectedCatalog, catalogs=catalogs)

# delete an item


@app.route('/catalog/<string:catalogName>/<string:itemName>/delete', methods=['GET', 'POST'])
def deleteItem(catalogName, itemName):
    item = session.query(Item).filter_by(itemName=itemName).one()
    if (request.method == 'POST'):
        session.delete(item)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteItem.html', item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
