Deployment
==========

The command ``python3 manage runserver`` is useful to check that the site looks ok, but it should not be
used in production, because the Django server is highly inefficient. You should rely on well-tested servers like
`Apache <https://httpd.apache.org/>`_ or `Nginx <https://www.nginx.com/>`_.

To publish your site so that other people can access it, you must properly set up a few critical entries in the ``.env``
file. Here are the key values that you should modify:

- Always set ``DEBUG`` to ``off``, otherwise any failure in the code will reveal important details about
  the internals of your site (e.g., secret keys, local paths…).

- Turn on ``LOGGING`` and specify a path where logging messages should be saved using the field
  ``LOG_FILE_PATH``; leave it out of the file if you want to send messages to the console. (This can be useful if
  your webserver already redirects console messages to a log file.) You can specify the style of the
  messages using the ``LOG_FORMATTER`` variable; it can either be ``brief`` (the default) or ``verbose``.

- Set up the logging level according to your tastes, using the field ``LOG_LEVEL``. Valid values are:

  1. ``DEBUG``
  2. ``INFO``
  3. ``WARNING``

  As an example, here is the section of a ``.env`` file where logging is configured::

    LOGGING=on
    LOG_FILE_PATH=/var/log/instrumentdb/instrumentdb.log
    LOG_FORMATTER=verbose
    LOG_LEVEL=INFO

- Set up a folder where to keep static files, e.g., ``/var/www/static``, and specify its path in the
  ``.env`` file, under the name ``STATIC_PATH``. Then, every time you update the site, be sure to
  run ``python3 manage.py collectstatic``, so that the path is filled with static files (images, CSS, etc.).
  You should make your webserver publish this folder under the URL ``/static``; see the `Django documentation
  <https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/modwsgi/#serving-files>`_ for an example.