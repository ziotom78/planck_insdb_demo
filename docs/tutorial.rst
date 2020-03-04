Tutorial
========

We are going to show how to use InstrumentDB through a simple tutorial
that will create and deploy the model of a ground-based experiment
for the observation of the Cosmic Microwave Background (CMB). The exact
nature of the experiment is not important for the example, but it helps
in making things more concrete.

What we are going to do
-----------------------

Here is a briew overview of this tutorial:

1. We must decide what kind of information we want to store in the database
   (:ref:`tut-what-information-to-store`);

2. Then, we will organize the information in a so-called `schema`, which
   tells InstrumentDB how to structure the data we are going to upload to
   the database (:ref:`tut-defining-a-schema`);

3. Once we implement the schema, we will upload data files to the
   server (:ref:`tut-upload-data-files`);

4. Finally, we will show how to access this information through the web
   interface and using the RESTful web API from the Python REPL
   (:ref:`tut-accessing-the-database`).

.. _tut-what-information-to-store:

What information to store
-------------------------

During the design phase of an instrument like the model described above,
several designs are attempted, and their value is judged depending on the
expected scientific outcome. Thus, the information to be stored in an
instrument model must be sufficient to simulate the behaviour of the
instrument to the point that this scientific outcome can be estimated
realistically.

In a typical CMB experiment, the microwave radiation coming from the
sky is collected by an optical system into feed horns, which convert
free propagation of the photons into guided propagation. At the end
of the acquisition chain, the radiation is measured by detectors and
saved in files. We can thus list the items that should be stored in our
instrument model:

- Sky region that the instrument will observe;
- Specification of the optical response for each feed;
- Noise level of each acquisition chain;
- Bandshape response of the detectors.

In the next section, we will show how to organize these items into a
database structure that can be managed by InstrumentDB.

.. _tut-defining-a-schema:

Defining a schema
-----------------

InstrumentDB organizes information according to the following concepts:

Format specification
   Every kind of information that will be stored in the database should be
   properly documented. To enforce this, InstrumentDB keeps a list of
   documents that describe the format used for files stored in the database.
   Several document types are recognized: PDF, Markdown, HTML, Word files, etc.

Entity
   An entity refers to some part of the instrument. In our example, an
   acquisition chain is an entity, as well as the telescope. Entities
   can be nested, so that the entity «acquisition chain» can contain the
   entities «filter» and «amplifier».

Quantity
   A measurable feature of an entity. If the entity is an «amplifier»,
   the quantity might be the amplifier's calibration curve, or its
   datasheet. Strictly speaking, a «quantity» is not really a concrete number,
   because these are provided by `data files` (see below). However, InstrumentDB
   permits users to query quantities for concrete numbers, as it has a
   way to associate quantities to data files.
   Several quantities can be associated to an entity.

Data file
   This is where the real data are stored. A data file can be anything the user
   wants: an Excel spreadsheet, a JSON metadata, a full thermal model, etc.
   Data files must be associated to quantities. InstrumentDB keep a version
   history of data files, so that they can be updated whenever required.
   It is possible to specify dependencies between data files: for instance,
   the data file of the calibration curve of an amplifier might state a
   dependency on a data file containing the data sheet of the amplifier
   itself.

Release
   Once in a while, the design of an instrument needs to be updated. This
   can happen after an extensive test campaign of the real hardware, or
   when some changes in the design of the instrument must be adopted to
   ensure the fullfillment of the scientific goals, or to face budget limits.
   InstrumentDB provides the ability to group data files into «releases»,
   which are tagged with an unique name and whose data files can be accessed
   through that name.

In our example, we might think of the following structure for our entities:

- Telescope

  - Optical model (quantity)
  - Thermal model (quantity)
  - Sky observation strategy (quantity)

- Acquisition chain

  - Detector A

    - Amplifier

      - Calibration curve (quantity)
      - Data sheet (quantity)

    - Bandshape response (quantity)

  - Detector B

    - Amplifier

      - Calibration curve (quantity)
      - Data sheet (quantity)

    - Bandshape response (quantity)

The safest way to define the structure of entities is through a YAML file.
InstrumentDB has the ability to read a YAML file and populate the database
with its contents. Users have still the possibility to manually create
each entity and quantity using the web interface, but for deeply-nested
structures like the one above, it is better to go through a text file.

We must first define the list of specification document for each quantity.
The structure above assumes the following data formats:

- Optical models; these might be proprietary files produced by some
  simulation software like GRASP, for instance. The specification document
  might well be the user's manual of the software, or a short technical
  note detailing the assumptions that must be used in the creation of the
  optical model (e.g., handedness of the coordinate system, measure units,
  etc.).
- Thermal models; again, these are usually proprietary files.
- Calibration curves for the amplifiers; we can assume that they are saved
  in CSV files. The format specification might be a text file specifying
  what's in each column, and what are the assumptions used in the calculation
  of these curves.
- Data sheets for the amplifiers: we can assume this is the PDF file provided
  by the vendor.
- Bandshape response: usually a bandshape is encoded as a two-column table
  that specifies the frequency and the response at that frequency.

Let's assume that we have already collected all the documents listed above.
Open a text editor and write the following YAML text:

.. code-block:: yaml

  format_specifications:
    - document_ref: "DOC-0001-OPTICAL-MODEL"
      title: "Optical models to be used in the experiment"
      file_mime_type: "application/octet-stream"
      doc_mime_type: "application/pdf"
      doc_file: "optical_model_specifications.pdf"
    - document_ref: "DOC-0001-THERMAL-MODEL"
      title: "Thermal models to be used in the experiment"
      file_mime_type: "application/octet-stream"
      doc_mime_type: "application/pdf"
      doc_file: "thermal_model_specifications.pdf"

.. code-block:: yaml

   entities:
     - name: "telescope"
       quantities:
         - name: "optical_model"
           format_spec: "DOC-0001-OPTICAL-MODEL"
         - name: "thermal_model"
           format_spec: "DOC-0002-THERMAL-MODEL"
         - name: "sky_observation_strategy"
           format_spec: "DOC-0003-OBS-STRATEGY"
     - name: "acquisition_chain"
       children:
         - name: "detector_A"
           children:
             - name: "amplifier"
               quantities:
               - name: "calibration_curve"
                 format_spec: "DOC-0004-CAL-CURVES"
               - name: "data_sheet"
                 format_spec: "DOC-0005-AMPLIFIER-SPECS"
           quantities:
             - name: "bandshape"
               format_spec: "DOC-0006-BANDSHAPE"
         - name: "detector_B"
           children:
             - name: "amplifier"
               quantities:
               - name: "calibration_curve"
                 format_spec: "DOC-0004-CAL-CURVES"
               - name: "data_sheet"
                 format_spec: "DOC-0005-AMPLIFIER-SPECS"
           quantities:
             - name: "bandshape"
               format_spec: "DOC-0006-BANDSHAPE"


Now, you have to tell InstrumentDB to create these entities and quantities
in the database.

.. _tut-upload-data-files:

Upload data files
-----------------

.. _tut-accessing-the-database:

Accessing the database
----------------------
