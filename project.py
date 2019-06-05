#!/usr/bin/env python3

from flask import Flask, request, render_template, make_response, jsonify, redirect, url_for, flash

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from database_setup import Catalog, Item, Base, User

from flask import session as login_session
import random
import string

# IMPORTS FOR gconnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

# json for items for a specific catalog


@app.route('/catalog/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']

    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'

        login_session['access_token'] = credentials.access_token
        login_session['gplus_id'] = gplus_id
        flash("you are now logged in as %s" % login_session['username'])

        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    # return output
    return redirect(url_for('showCatalog', username=login_session['username']))


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        return redirect(url_for('showCatalog'))

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("you are now logged out now")
        return redirect(url_for('showCatalog'))
    else:
        return redirect(url_for('showCatalog'))


# User helper functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/catalog/<string:catalogName>/items/JSON')
def catalogItemsJSON(catalogName):
    catalog = session.query(Catalog).filter_by(catalogName=catalogName).one()
    items = session.query(Item).filter_by(
        catalog_id=catalog.id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/catalog/<string:catalogName>/<string:itemName>/JSON')
def itemJSON(catalogName, itemName):
    item = session.query(Item).filter_by(itemName=itemName).one()
    return jsonify(Item=item.serialize)


@app.route('/catalog/JSON')
def itemsJSON():
    items = session.query(Item).all()
    return jsonify(restaurants=[i.serialize for i in items])

# show all catalog


@app.route('/')
@app.route('/catalog')
def showCatalog():
    catalogs = session.query(Catalog).all()

    if 'username' in login_session:
        items = session.query(Item.itemName, Catalog.catalogName).filter(
            Item.catalog_id == Catalog.id).filter(or_(Item.user_id == 1, Item.user_id == login_session['user_id'])).order_by(Item.id.desc()).limit(3)
    else:
        items = session.query(Item.itemName, Catalog.catalogName).filter(
            Item.catalog_id == Catalog.id).filter(Item.user_id == 1).order_by(Item.id.desc()).limit(3)

    return render_template("catalog.html", catalogs=catalogs, items=items)

# show all items for a specific catalog


@app.route('/catalog/<string:name>')
@app.route('/catalog/<string:name>/items')
def showCatalogItems(name):
    catalogs = session.query(Catalog).all()
    catalog = session.query(Catalog).filter_by(
        catalogName=name.replace('-', ' ')).one()
    if 'username' in login_session:
        items = session.query(Item).filter_by(catalog_id=catalog.id).filter(
            or_(Item.user_id == 1, Item.user_id == login_session['user_id'])).all()
    else:
        items = session.query(Item).filter_by(
            catalog_id=catalog.id).filter_by(user_id=1).all()
    return render_template("items.html", catalogs=catalogs, items=items, selected_catalog=catalog)


# show an item
@app.route('/catalog/<string:catalogName>/<string:itemName>')
def showItemName(catalogName, itemName):
    creator = True

    item = session.query(Item).filter_by(itemName=itemName).one()
    catalog = session.query(Catalog).filter_by(
        catalogName=catalogName.replace('-', ' ')).one()
    # local permission, one user can not see other user's content
    if item.user_id != 1:
        if 'username' not in login_session or login_session['user_id'] != item.user_id:
            response = make_response(json.dumps(
                "you are not allowed to see this page"), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

    if 'username' not in login_session or login_session['user_id'] != item.user_id:
        creator = False
    return render_template('item.html', item=item, catalog=catalog, creator=creator)

# create a new item


@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        response = make_response(json.dumps(
            "you must login first to add new item"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if (request.method == 'POST'):
        catalog = session.query(Catalog).filter_by(
            catalogName=request.form['catalogname']).one()
        newItem = Item(itemName=request.form['coinname'], description=request.form['description'],
                       catalog_id=catalog.id, user_id=login_session['user_id'])
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
    if 'username' not in login_session or item.user_id != login_session['user_id']:
        response = make_response(json.dumps(
            "you are not allowed to edit this page"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
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
    if 'username' not in login_session:
        response = make_response(
            json.dumps("you are not allowed to make delete operation"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

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
