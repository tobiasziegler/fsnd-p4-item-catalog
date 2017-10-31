from models import Base, Category, Item
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask import Flask, render_template

engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/')
@app.route('/catalog')
def showCatalog():
    return render_template('catalog.html')


@app.route('/catalog/categories/<category>')
def showCategory(category):
    return render_template('showCategory.html', category=category)


@app.route('/catalog/categories/<category>/items/<item>')
def showItem(category, item):
    return render_template('showItem.html', category=category, item=item)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
