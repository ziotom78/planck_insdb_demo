Installation
============

Prerequisites
-------------

You need to have Python 3 installed on your system. You should have
`pip` and `virtualenv` installed; on Debian/Ubuntu/Mint systems,
install them using the command::

  sudo apt install python3-pip python3-virtualenv


Step-by-step procedure
----------------------

Before installing InstrumentDB, you should first decide if you just
want to *use* it («User's install»), or if you are likely going to
hack it («Developer's install»).

If you do not know which option to pick, you are surely going to be a
*user*, so go on with «User's install».

User's install
~~~~~~~~~~~~~~


To install InstrumentDB, follow these steps:

1. Create and activate a virtual environment::

    virtualenv venv
    source venv/bin/activate
   
2. Download the source code::

    git clone https://github.com/ziotom78/instrumentdb.git && cd instrumentdb

3. Install all the dependencies (you must have a working Internet
   connection to run this)::

    pip3 install -r requirements.txt   

3. Create a custom configuration file and customize it. Be sure to put some
   random password in ``SECRET_KEY``::

    cp .env.example .env && vim .env

4. Create an empty database::

    python3 manage.py migrate

5. Create a superuser::

    python3 manage.py createsuperuser

   Be sure to note down the username and password you pick here, because
   they will be required to log in.

6. Test that everything works by firing the local webserver with the following
   command::

    python3 manage.py runserver

   Connect to http://127.0.0.1:8000/. If you see an empty landing page, it means
   that InstrumentDB is operative. Congratulations!

   
Developer's install
~~~~~~~~~~~~~~~~~~~

If you are reading this section, it means that you are planning to
work on InstrumentDB's source code. First install `Poetry
<https://python-poetry.org/>`_, the tool used to manage dependencies
in this project.

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

    poetry run ./manage.py migrate

5. Create a superuser::

    poetry run ./manage.py createsuperuser

   Be sure to note down the username and password you pick here, because
   they will be required to log in.

6. Test that everything works by firing the local webserver with the following
   command::

    poetry run ./manage.py runserver

   Connect to http://127.0.0.1:8000/. If you see an empty landing page, it means
   that InstrumentDB is operative. Congratulations!
