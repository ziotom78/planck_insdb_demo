Introduction to InstrumentDB
============================

Welcome! InstrumentDB is a web-based application that can be used
to store information about a scientific experiment. It lets the user
to easily save and retrieve things like the following:

- Calibration curves
- Datasheets of electronic components
- Noise properties of components
- Thermal models
- Optical model of a telescope
- Etc.

This kind of information is vital during the life cycle of a scientific
experiment:

1. When an instrument is being designed, the so-called `instrument model`
   is the input to simulation codes that estimate the scientific outcome
   of the experiment, thus validating its design.
2. When an instrument is operative, the data in the instrument model are
   used to properly reduce the raw data acquired by the instrument into
   scientific results.

InstrumentDB provides the tools necessary to keep this instrument model
organized and easy to access. It does not force the user to follow a rigid
structure for their data; on the contrary, it is extremely versatile and
customizable.

A typical pattern to use InstrumentDB is the following:

1.  Install InstrumentDB on a computer;
2.  Define the database schema, that is, the structure of the data you
    are going to manage using InstrumentDB. For instance, are you going
    to save datasheets of electronic parts? or just calibration curves?
3.  Upload the necessary data files in the database (optical models,
    noise properties, etc.), populating the structure you defined in the
    previous step;
4.  Start the InstrumentDB server;
5.  Either access InstrumentDB through a web browser or through its
    RESTful API.
