Releases
========

A «release» is a way to bundle together a coherent set of data files
in the instrument database. It is a common situation when designing an
instrument that its characteristics keep changing, because of a
variety of reasons (e.g., additional funding enables to use better
hardware components, hardware tests permit to better characterize the
instrument, etc.).

InstrumentDB keeps track of all the versions for each data file. This
is vital to ensure the traceability of the characteristics of the
instrument as well as a way to record its evolution. However, the
presence of several versions for a data file can easily complicate
things: if there are two versions A and B of a data file containing
the noise characteristics of a detector, and three versions 1, 2, and
3 of the bandpass for the same detector, what should a simulation code
use as input? Should it use (A, 1), (B, 1), (A, 2), or whatever else?

Release tags are a way to assign the same label to several data files,
with the aim to mark them as different bits of information for the
same design. They can be named using an unique identifier containing
letters, numbers, the underscore and the dot. Good names are
``grant_proposal``, ``v1.3``, ``final``, etc.
