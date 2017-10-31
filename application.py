from models import Base, User, Category, Item
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine, desc, asc
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from slugify import slugify

CLIENT_ID = json.loads(
    open('google_client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog App"

engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


# Create a state token to prevent request forgery.
# Store it in the session for later validation.
@app.route('/login')
def showLogin():
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
        oauth_flow = flow_from_clientsecrets('google_client_secret.json',
                                             scope='')
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
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(json.dumps(
                                 'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists. If it doesn't, make a new one.
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
    output += (' " style = "width:300px; height: 300px;border-radius:150px;'
               '-webkit-border-radius:150px;-moz-border-radius: 150px;">')
    flash("You are now logged in as %s" % login_session['username'])
    print("done!")
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
    except NoResultFound:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s' % access_token)
    print('User name is: ')
    print(login_session['username'])
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['google_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
                                 'Failed to revoke token for given user.',
                                 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(desc(Item.id)).limit(10).all()
    return render_template('catalog.html', categories=categories, items=items)


@app.route('/catalog/categories/<category_slug>')
def showCategory(category_slug):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(slug=category_slug).first()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('showCategory.html', categories=categories,
                           category=category, items=items)


@app.route('/catalog/categories/new',
           methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        slug = slugify(name)
        newCategory = Category(name=name,
                               slug=slug,
                               user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCategory.html')


@app.route('/catalog/categories/<category_slug>/edit',
           methods=['GET', 'POST'])
def editCategory(category_slug):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(Category).filter_by(
                        slug=category_slug).first()
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
            slug = slugify(name)
            editedCategory.name = name
            editedCategory.slug = slug
            session.add(editedCategory)
            session.commit()
            flash('Category %s Successfully Edited' % editedCategory.name)
            return redirect(url_for('showCatalog'))
    else:
        return render_template('editCategory.html', category=editedCategory)


@app.route('/catalog/categories/<category_slug>/delete',
           methods=['GET', 'POST'])
def deleteCategory(category_slug):
    if 'username' not in login_session:
        return redirect('/login')
    categoryToDelete = session.query(Category).filter_by(
                       slug=category_slug).one()
    if request.method == 'POST':
        itemsToDelete = session.query(Item).filter_by(
                        category=categoryToDelete).all()
        for i in itemsToDelete:
            session.delete(i)
        session.delete(categoryToDelete)
        flash('Category %s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteCategory.html',
                               category=categoryToDelete)


@app.route('/catalog/categories/<category_slug>/items/<item_slug>')
def showItem(category_slug, item_slug):
    category = session.query(Category).filter_by(slug=category_slug).first()
    item = session.query(Item).filter_by(slug=item_slug).first()
    return render_template('showItem.html', category=category, item=item)


@app.route('/catalog/categories/<category_slug>/items/new',
           methods=['GET', 'POST'])
def newItem(category_slug):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(slug=category_slug).first()
    if request.method == 'POST':
        name = request.form['name']
        slug = slugify(name)
        description = request.form['description']
        newItem = Item(name=name,
                       slug=slug,
                       description=description,
                       user_id=login_session['user_id'],
                       category_id=category.id)
        session.add(newItem)
        flash('New Item %s Successfully Created' % newItem.name)
        session.commit()
        return redirect(url_for('showCategory', category_slug=category_slug))
    else:
        return render_template('newItem.html', category=category)


@app.route('/catalog/categories/<category_slug>/items/<item_slug>/edit',
           methods=['GET', 'POST'])
def editItem(category_slug, item_slug):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(
                   slug=category_slug).first()
    editedItem = session.query(Item).filter_by(
                     slug=item_slug).first()
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
            slug = slugify(name)
            description = request.form['description']
            editedItem.name = name
            editedItem.slug = slug
            editedItem.description = description
            session.add(editedItem)
            session.commit()
            flash('Item %s Successfully Edited' % editedItem.name)
            return redirect(url_for('showCategory',
                                    category_slug=category_slug))
    else:
        return render_template('editItem.html', category=category,
                               item=editedItem)


@app.route('/catalog/categories/<category_slug>/items/<item_slug>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_slug, item_slug):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(
                   slug=category_slug).first()
    itemToDelete = session.query(Item).filter_by(
                       slug=item_slug).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('Item %s Successfully Deleted' % itemToDelete.name)
        session.commit()
        return redirect(url_for('showCategory', category_slug=category_slug))
    else:
        return render_template('deleteItem.html', category=category,
                               item=itemToDelete)


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
