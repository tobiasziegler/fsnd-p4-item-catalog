# Item Catalog

This web app accesses a database of categorised items, allowing the public to
browse the catalog, and allowing authorised users to create, update and delete
items and categories. I've created this program as part of the [Full Stack Web
Developer Nanodegree.](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

## Getting Started

1. Download, clone or fork this repository to an appropriate location on your
server or virtual machine.

1. Ensure you have the required software dependencies:

    1. Python 3

    1. PostgreSQL

    1. [`python-slugify`](https://github.com/un33k/python-slugify) (e.g., `pip3 install python-slugify`)

1. Create or download a `google_client_secret.json` file in the project
directory containing OAuth credentials for the app. If I haven't supplied you
with my credentials for the app, then you need to create your own via the
Google Developer Console as follows:

    1. Authorized origins should include `http://localhost:5000` (or modify if
        not running locally)

    1. Authorized redirect URIs should include `http://localhost:5000/postmessage`

    1. If you create your own credentials, also update the app ID in `login.html`

1. Create the database: `psql -d catalog`

1. Add sample data to the database - from the project directory, run
`python3 populate_database.py`.

1. Run the app using `python3 application.py`.

1. Load the app locally at `http://localhost:5000`.

## API endpoints

There are three API calls available to retrieve data in JSON format:

1. `/api/categories` returns a list of all categories

1. `/api/categories/<category_slug>` returns all items in the specified category

1. `/api/categories/<category_slug>/items/<item_slug>` returns the specified
item
