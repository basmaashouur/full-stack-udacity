# imports
from flask import Flask, render_template, url_for
from flask import request, redirect, flash, jsonify, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from dbsetup import *
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os
import random
import string
import datetime
import json
import httplib2
import requests


# Flask instance
app = Flask(__name__)


# GConnect CLIENT_ID
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item-Catalog"


# Connect to database
engine = create_engine('sqlite:///catlogitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Login - Create anti-forgery state token
@app.route('/login/')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase+string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# GConnect
@app.route('/gconnect/', methods=['POST'])
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
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

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
        response = make_response(json.dumps('user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
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
    return output


# User Helper Functions


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


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect/')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = redirect("/catalog/")
        flash("You are now logged out.")
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Home page
@app.route('/')
@app.route('/catalog/')
def showCatlog():
    category = session.query(Category).all()
    latestitems = session.query(Item).order_by(desc(Item.date)).limit(5)
    if 'username' not in login_session:
        return render_template("publiccatalog.html", category=category,
                               latestitems=latestitems)
    else:
        return render_template("catalog.html", category=category,
                               latestitems=latestitems)


# Add a new  catgeory
@app.route('/catalog/new/', methods=['GET', 'POST'])
def addCategory():
    if 'username' not in login_session:
        return redirect('/login/')
    if request.method == 'POST':
        newcate = Category(
            title=request.form['title'], user_id=login_session['user_id'])
        session.add(newcate)
        flash('New Category %s Successfully Created' % newcate.title)
        session.commit()
        return redirect("/catalog/")
    else:
        return render_template('newcategory.html')


# Show the categogry
@app.route('/catalog/<int:category_id>/')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return render_template('publiccategory.html', category=category)
    else:
        return render_template('category.html', category=category)


# Show the items in that category id
@app.route('/catalog/<int:category_id>/items/')
def showItems(category_id):
    categoryall = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    if 'username' not in login_session:
        return render_template("publicitems.html", category=category,
                               items=items, categoryall=categoryall)
    else:
        return render_template("items.html", category=category,
                               items=items, categoryall=categoryall)


# Edit a category
@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editcate = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login/')
    if editcate.user_id != login_session['user_id']:
        flash("You cannot edit this Category. This Category belongs to you")
        return redirect("/catalog/")
    if request.method == 'POST':
        editcate.title = request.form['title']
        session.add(editcate)
        session.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('editcategory.html', category_id=category_id)


# Delete a category
@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    delcate = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login/')
    if delcate.user_id != login_session['user_id']:
        flash("You cannot delete this Category. This Category belongs to you")
        return redirect("/catalog/")
    if request.method == 'POST':
        session.delete(delcate)
        session.commit()
        return redirect("/catalog/")
    else:
        return render_template('deletecategory.html', category_id=category_id)


# Add a new Item
@app.route('/catalog/<int:category_id>/newitem/', methods=['GET', 'POST'])
def addItem(category_id):
    if 'username' not in login_session:
        return redirect('/login/')
    if request.method == 'POST':
        cattitle = session.query(Category).filter_by(id=category_id).one()
        newitem = Item(title=request.form['title'],
                       description=request.form['description'],
                       img=request.form['img'],
                       category_id=category_id,
                       user_id=login_session['user_id'],
                       date=datetime.datetime.now(),
                       cattitle=cattitle.title)
        session.add(newitem)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)


# Show item deatils
@app.route('/catalog/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return render_template("publicitem.html", item=item)
    else:
        return render_template("item.html", item=item)


# Edit an item
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    edititem = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login/')
    if edititem.user_id != login_session['user_id']:
        flash("You cannot edit this item. This item belongs to you")
        return redirect("/catalog/")
    if request.method == 'POST':
        if request.form['title']:
            edititem.title = request.form['title']
        if request.form['description']:
            edititem.description = request.form['description']
        if request.form['img']:
            edititem.img = request.form['img']
        session.add(edititem)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id,
                                item_id=item_id))
    else:
        return render_template("edititem.html", category_id=category_id,
                               item_id=item_id)


# Delete an item
@app.route('/catalog/<int:category_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    delitem = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login/')
    if delitem.user_id != login_session['user_id']:
        flash("You cannot delete this item. This item belongs to you")
        return redirect("/catalog/")
    if request.method == 'POST':
        session.delete(delitem)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteitem.html', category_id=category_id,
                               item_id=item_id)


# JSON APIs to view Catalog Information


# Displays the whole Categories
@app.route('/catalog/JSON/')
def categoryJSON():
    Catgories = session.query(Category).all()
    return jsonify(Catgories=[r.serialize for r in Catgories])


# Displays items for a specific category
@app.route('/catalog/<int:category_id>/items/JSON/')
def restaurantMenuJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# Displays a specific category item.
@app.route('/catalog/<int:category_id>/<int:item_id>/JSON/')
def menuItemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=category_id).one()
    return jsonify(item=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
