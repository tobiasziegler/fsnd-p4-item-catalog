from flask import Flask, render_template
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
