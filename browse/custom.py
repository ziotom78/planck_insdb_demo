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
import json

from browse.models import Entity


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
    cur_release = context["object"].tag

    for instrument in ("LFI", "HFI"):
        cur_quantity = Entity.objects.get(name=instrument).quantities.get(
            name="full_focal_plane"
        )

        data_files = cur_quantity.data_files.filter(release_tags__tag=cur_release)
        if len(data_files) != 1:
            continue

        data_file = data_files[0]
        cur_metadata = json.loads(data_file.metadata)

        context[instrument] = list(cur_metadata.values())


# This is used to prepare the context for the template
# borwse/templates/browse/release_list.html
def create_release_listview_context(context):
    """Create the context to render a :class:`ReleaseListView`"""
    pass
