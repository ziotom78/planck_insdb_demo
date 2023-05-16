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
  ``LOG_FILE_PATH``; be sure that the directory where you save this file is writable.
