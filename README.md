# TopHandball website
This repository holds the Django app that powers women's handball website TopHandball.com

## Contributing
Contributions are welcome either as pull requests or by reporting issues.

### Setting up a development environment

Clone the repository:

    git clone git@github.com:lhuriguen/tophandball.git

Create a virtualenv anywhere you want and activate it.

Install the required packages for development:

    pip install -r requirements/dev.txt

Create the PostgreSQL database and user:

    sudo su - postgres
    createuser -P tophb
    createdb --owner=tophb tophb

Alternatively, you can configure your own database URL with environment variables. See [dj-database-url](https://github.com/kennethreitz/dj-database-url) for more info.

Create the database structure:

    ./manage.py migrate

Run the local server:

     ./manage.py runserver
