# -*- encoding: utf-8 -*-

"""
This file enables the user to customize the appearance of several views.

The way it is supposed to be used is the following:

1. Fork the repository https://github.com/ziotom78/instrumentdb

2. Modify the HTML templates for the views you want to personalize (they are in
   browse/templates/)

3. Modify this file so that you provide context variables useful for the templates
   you personalized in step #2. You should usually start by getting an instance
   of the object that is being displayed, e.g., with the line

       cur_release = context["object"].tag

   in `create_release_view_context`

4. You can substitute the file browse/static/browse/logo.svg with your own logo

5. Deploy your fork using a webserver!
"""


# This is used to prepare the context for the template
# borwse/templates/browse/entity_detail.html
# The field context["object"] is the instance the Entity class
def create_entity_view_context(context):
    """Create the context to render a :class:`EntityListView`"""
    pass


# This is used to prepare the context for the template
# borwse/templates/browse/quantity_detail.html
# The field context["object"] is the instance the Quantity class
def create_quantity_view_context(context):
    """Create the context to render a :class:`QuantityView`"""
    pass


# This is used to prepare the context for the template
# borwse/templates/browse/datafile_detail.html
# The field context["object"] is the instance the DataFile class
def create_datafile_view_context(context):
    """Create the context to render a :class:`DataFileView`"""
    pass


# This is used to prepare the context for the template
# borwse/templates/browse/release_detail.html
# The field context["object"] is the instance the Release class
def create_release_view_context(context):
    """Create the context to render a :class:`ReleaseView`"""
    pass


# This is used to prepare the context for the template
# borwse/templates/browse/release_list.html
def create_release_listview_context(context):
    """Create the context to render a :class:`ReleaseListView`"""
    pass
