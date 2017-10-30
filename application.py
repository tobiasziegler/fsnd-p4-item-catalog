from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/catalog')
def showCatalog():
    return 'This page will show all categories and the latest added items'


@app.route('/catalog/categories/<category>')
def showCategory(category):
    return 'This page will show all items for the specified category'


@app.route('/catalog/categories/<category>/items/<item>')
def showItem(category, item):
    return 'This page will show specific information about the specified item'


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
