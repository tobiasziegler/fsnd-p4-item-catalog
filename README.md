# Item Catalog

This web app accesses a database of categorised items, allowing the public to
browse the catalog, and allowing authorised users to create, update and delete
items and categories.

## Getting Started

1. Download, clone or fork this repository to an appropriate location on your
server or virtual machine.

1. Ensure you have the required software dependencies:

    1. Python 3

    1. PostgreSQL

    1. [`python-slugify`](https://github.com/un33k/python-slugify) (e.g., `pip3 install python-slugify`)

1. Create the database: `psql -d catalog`

1. Add sample data to the database - from the project directory, run
`python3 populate_database.py`.

1. Run the app using `python3 application.py`.

1. Load the app locally at `http://localhost:5000`.
