Installation
============

Prerequisites
-------------

You need to have Python 3 and `Poetry <https://python-poetry.org/>`_ installed on your system.

Step-by-step procedure
----------------------

To install InstrumentDB, follow these steps:

1. Download the source code::

    git clone https://github.com/ziotom78/instrumentdb.git && cd instrumentdb

2. Install all the dependencies (you must have a working Internet
   connection to run this)::

    poetry install

3. Create a custom configuration file and customize it. Be sure to put some
   random password in ``SECRET_KEY``::

    cp .env.example .env && vim .env

4. Create an empty database::

    poetry run manage.py migrate

5. Create a superuser::

    poetry run manage.py createsuperuser

   Be sure to note down the username and password you pick here, because
   it will be required every time you want to access the `admin` interface.

6. Test that everything works by firing the local webserver with the following
   command::

    poetry run manage.py runserver

   Connect to http://127.0.0.1:8000/. If you see an empty landing page, it means
   that InstrumentDB is operative. Congratulations!