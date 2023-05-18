Customizing the site
====================

The best way to customize InstrumentDB is to fork the repository https://github.com/ziotom78/instrumentdb and apply
one's own modifications to the fork. The things that one would probably modify are the following:

1. The logo that appears on the top left corner of every page of the site;
2. The appearance of single HTML pages

Changing the logo
-----------------

The logo is stored in the folder ``browse/static/browse/logo.svg``, and it can
be overwritten; other formats than SVG can of course be used, but in this case
the name of the file should be changed and thus the template ``browse/templates/base_generic.html`` should
be modified too.

Customizing HTML pages
----------------------

The templates of the HTML page that are used to display information about entities/quantities/data files/releases/etc.
are stored in ``browse/templates/browse``. If you want to modify them, you are probably going to need some more
“context”, i.e., additional information in the page that should be taken from the database. (For instance, you might
want to grab some numbers from a CSV file and insert a HTML table in the page itself, so that the
user can see the data without the need to first download the data file.)

In this case, you will need to modify ``browse/custom.py``: this file is going to be changed rarely, and thus
your fork should not be affected by future updates to the code. The file implements a number of empty functions
like ``create_datafile_view_context``::

    def create_datafile_view_context(context):
        """Create the context to render a :class:`DataFileView`"""
        pass

The parameter `context` is a dictionary that you can modify by adding new fields; these will be made
available in the corresponding HTML template, so that you can pass additional information grabbed from the database.

Here is an example that shows a possible customization: we want to put a custom message in the page that shows
information about a data file if the metadata contain the key ``margin``; in this case, we want the value of the key to
be displayed in the message.

Here is how we should modify ``create_datafile_view_context``::

    def create_datafile_view_context(context):
        """Create the context to render a :class:`DataFileView`"""
        cur_datafile = context["object"]

        import json
        metadata_dict = json.loads(cur_datafile.metadata)
        try:
            context["margin"] = metadata_dict["margin"]
        except KeyError:
            # No key "margin", what a pity!
            pass

And we should of course use the new keyword ``margin`` that has been added to ``context`` by referring to it somewhere in the
HTML template ``browse/templates/browse/datafile_detail.html``:

.. code-block:: html

  <!-- Put this somewhere in the file
       browse/templates/browse/datafile_detail.html -->
  {% if margin %}
  <p>This data file has the “margin” field in the metadata,
  and its value is {{ margin }}.</p>
  {% endif %}
