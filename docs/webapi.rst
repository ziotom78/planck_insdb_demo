Web API
=======

This section provides the documentation to the web API implemented 

Format specifications
---------------------

You can query the list of format specifications by issuing a ``GET``
command to the url http://server/api/format_specs/. To get information
about one entity, append the full UUID and a slash to it:
http://server/api/format_specs/ede55e77-0dd1-483e-a307-e6e67759a450/.

To create a new entity, issue a ``POST`` command and pass a JSON
dictionary containing the following fields:

- ``document_ref``: a string uniquely identifying the document. The
  format of the string depends on the conventions used by the
  collaboration developing the instrument.
- ``title``: a string containing the title of the specification document.
- ``file_mime_type``: a string containing the MIME type of the file
  described by this specification document (optional).

Entities
--------

You can query the list of entities by issuing a ``GET`` command to the
url http://server/api/entities/. To get information about one entity,
append the full UUID and a slash to it:
http://server/api/entities/ede55e77-0dd1-483e-a307-e6e67759a450/.

To create a new entity, issue a ``POST`` command and pass a JSON
dictionary containing the following fields:

- ``name``: a string
- ``parent``: the full URL to the parent entity; leave it out if the
  entity has no parent.
- ``children``: a list of full URLS for the child entities; you can
  leave it out.

Here is an example in Python, it creates a new entity and then deletes
it immediately after::

  import requests

  server = "http://127.0.0.1:8000/"
  req = requests.post(server + "api/entities/", data={
      "name": "my entity",
  })
  print(req.json())

  # Output:
  # {'uuid': 'f89e8597-7561-4170-bec3-9837b3f32d61',
  #  'url': 'http://127.0.0.1:8000/f89e8597-7561-4170-bec3-9837b3f32d61/',
  #  'name': 'my entity',
  #  'parent': None,
  #  'children': [],
  #  'quantities': []}

  # Now delete the entity that was created above
  requests.delete(req.json()["url"])

To alter an object, you can use the ``PATCH`` command. The following
example creates an object and then modifies its name::
  
  import requests

  server = "http://127.0.0.1:8000/"
  req = requests.post(server + "api/entities/", data={
      "name": "my entity",
  })
  url = req.json()["url"]

  # This command changes "my entity" into "a better name"
  requests.patch(url, data={"name": "a better name"})
  
Quantities
----------

You can query the list of quantities by issuing a ``GET`` command to
the url http://server/api/quantities/. To get information about one
entity, append the full UUID and a slash to it:
http://server/api/quantities/ede55e77-0dd1-483e-a307-e6e67759a450/.

To create a new quantity, you must issue a ``POST`` command with a
JSON record containing these keys:

- ``name``: a string
- ``format_spec``: the URL to a format specification object
- ``parent_entity``: the URL to an entity


Data files
----------

You can query the list of data files by issuing a ``GET`` command to
the url http://server/api/data_files/. To get information about one
entity, append the full UUID and a slash to it:
http://server/api/data_files/ede55e77-0dd1-483e-a307-e6e67759a450/.

To create a new data file, you must issue a ``POST`` command with a
JSON record containing these keys:

- ``name``: a name to be used when the data file is going to be
  downloaded locally into an actual file.
- ``upload_date``: the date and time when the file was created. If not
  provided, the current date will be used.
- ``metadata``: a JSON structure containing custom metadata associated
  with the data file (optional).
- ``quantity``: the URL to the quantity that owns this data file.
- ``spec_version``: a custom string specifying which version of the
  specification document (associated with ``quantity``) was used to
  produce this data file (optional).
- ``dependencies``: a list of URLs to data files that have been used
  to produce this very data file (optional).
- ``plot_mime_type``: the MIME type of the plot associated with this
  data file (optional).
- ``comment``: a string containing any comment (optional).
- ``release_tags``: a list of URLS to the releases that include this
  data file (optional).
  
Releases
--------

You can query the list of releases by issuing a ``GET`` command to the
url http://server/api/releases/. To get information about one release,
append its name and a slash to it: http://server/api/releases/v0.28/.

To create a new release, you must issue a ``POST`` command with a
JSON record containing these keys:

- ``tag``: the name of the release. The only characters allowed here
  are letters, digits, the underscore and the dot.
- ``rel_date``: the date when the release was created. If not
  specified, the current date is used.
- ``comments``: a string containing any useful comment regarding this
  release (optional).
- ``data_files``: a list of URLs containing the data files.

To associate data files to releases, you can use one of the following
approaches:

1. Add data files to the release tag as soon as you create it;
2. Add data files to the release tag after having created the release;
3. Add releases to a data file.

Let's see each of the three approaches. The first one is the simplest::

  import requests

  server = "http://127.0.0.1:8000/"

  # Name of the release we're going to create
  release_name = "v0.10"

  # These are the data files to be added to the release
  data_files = [
      "http://127.0.0.1:8000/api/data_files/021d0dfa-e54a-44ca-abc8-ac1d01ed4c50/",
      "http://127.0.0.1:8000/api/data_files/791a310e-f950-4370-bcf0-bc49622847c9/",
      "http://127.0.0.1:8000/api/data_files/34c11186-2ce2-4805-9114-91ed460c6a95/",
  ]
  # Create the release
  req = requests.post(server + "api/releases/", data={
      "tag": release_name,
      "comment": "dummy release",
      "data_files": data_files,
  })

Let's now consider the case where you did not pass the ``data_files``
key in the POST command above. (For instance, you were still building
the list of data files.) Assuming that a release was already created,
you can use ``PATCH`` commands to modify the release object, as shown
in this snippet::

  # We are re-using the "req" object got in the snippet above through
  # the call to `requests.post`
  release_info = req.json()
  
  # This is the URL of the release we created
  url = req.json()["url"]
  
  # We are re-using "tag" and "comment" from the call to `request.post`
  # above, but we might change them as well in this call, as the HTTP
  # `patch` command overwrites everything.
  requests.patch(url, data={
      "tag": release_info["tag"],
      "comment": release_info["comment"],
      "data_files": data_files,
  })
  
Alternatively, we can go through the opposite route and add the
release tag to every data file in the list ``data_files``. The
following snippet is equivalent to the code above::

  for cur_data_file_url in data_files:
      # Retrieve the current data file
      cur_data_file = requests.get(cur_data_file_url).json()

      # Append the URL to the new release to the list of release tags
      cur_data_file["release_tags"].append(release_info["url"])

      # Modify the data file in the database
      requests.patch(cur_data_file_url, data=cur_data_file)
