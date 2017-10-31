from models import Base, User, Category, Item
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, desc
from flask import Flask, render_template, url_for

engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


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


@app.route('/catalog/categories/<category_slug>/items/<item_slug>')
def showItem(category_slug, item_slug):
    category = session.query(Category).filter_by(slug=category_slug).first()
    item = session.query(Item).filter_by(slug=item_slug).first()
    return render_template('showItem.html', category=category, item=item)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
