# -*- encoding: utf-8 -*-

"""Implementation of the fundamental concepts of an IMO as database
tables.

This file implements the following classes, which are descendeants of
Django's `models.Model` class and are therefore used to set up tables
in the database:

- `Entity`: a feature of the instrument that is modelled in the
  IMO. Entities can form tree-like structures. Examples: a telescope,
  a cryostat, a focal plane, a beam, etc., where focal planes can be
  parents of several beams.

- `Quantity`: numerical information related to an entity, which must
  conform to some format specification (see below). Examples: a beam
  pattern saved as a Healpix map, a bandpass stored in an Excel file,
  etc.

- `FormatSpecification`: a document that presents the mathematical
  model, the units of measure used, the assumptions, and the file
  format used for files storing a "quantity" (see above)

- `DataFile`: a file containing numerical estimates of some
  "quantity" (see above).

"""

import uuid
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Entity(models.Model):
    name = models.CharField(
        max_length=256, help_text="Descriptive name for this entity"
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    ordering = ("name",)

    def __str__(self):
        return self.name


class FormatSpecification(models.Model):
    document_ref = models.CharField(
        "ID of the specification document",
        max_length=64,
        unique=True,
        help_text="ID of the technical document",
    )
    title = models.CharField(
        max_length=256,
        help_text="Title of the document containing the specification "
        + "for a file format",
    )
    doc_file = models.FileField(
        "Specification document",
        null=True,
        blank=True,
        help_text="Downloadable copy of the specification document (optional)",
    )
    # Regarding the maximum length of a MIME type, see
    # https://stackoverflow.com/questions/643690/maximum-mimetype-length-when-storing-type-in-db
    doc_mime_type = models.CharField(
        "MIME type of the specification document",
        max_length=256,
        help_text="This specifies the MIME type of the downloadable copy "
        + "of the specification document",
    )
    file_mime_type = models.CharField(
        "MIME type of the file",
        max_length=256,
        help_text="This specifies the MIME type of the data file",
    )

    def __str__(self):
        if self.title:
            return f'{self.document_ref} ("{self.title}")'
        else:
            return f"{self.document_ref}"


class Quantity(models.Model):
    uuid = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(
        max_length=256, help_text="Descriptive name for this quantity"
    )
    format_spec = models.ForeignKey(
        FormatSpecification,
        on_delete=models.CASCADE,
        help_text="Reference to the format specification used for data files "
        + "associated with this quantity",
    )
    parent_entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        help_text="Entity to whom this quantity is related",
    )

    ordering = (
        "name",
        "uuid",
    )

    def __str__(self):
        return f"{self.name} ({self.uuid[0:8]})"


class DataFile(models.Model):
    uuid = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(
        "file name", max_length=1024, default="noname", help_text="Name of the file"
    )
    upload_date = models.DateTimeField(
        "date when the file was uploaded",
        default=timezone.now,
        editable=False,
        help_text="Date when the file was added to the database",
    )
    metadata = models.TextField(
        "JSON-formatted metadata",
        max_length=8192,
        blank=True,
        help_text="JSON record containing metadata for the file",
    )
    file_data = models.FileField(
        "File", blank=True, help_text="File contents (when present)"
    )
    quantity = models.ForeignKey(
        Quantity,
        on_delete=models.CASCADE,
        help_text="Quantity associated with the data in this file",
    )
    spec_version = models.CharField(
        "version of the specification document",
        max_length=32,
        help_text="Version number of the format specification document",
    )
    dependencies = models.ManyToManyField(
        "DataFile",
        blank=True,
        help_text="List of data files that have been used as inputs to "
        + "produce this data file",
    )
    plot_file = models.FileField(
        "Image file", blank=True, help_text="Plot of the data in the file (optional)"
    )
    plot_mime_type = models.CharField(
        "MIME type of the image",
        max_length=256,
        blank=True,
        help_text="This specifies the MIME type of the image",
    )

    comment = models.TextField(max_length=4096, blank=True, help_text="Free-form notes")

    # When querying *all* the DataFile objects in a database, the
    # (inverse) order by upload date will not be very meaningful… But
    # usually we query only for DataFile objects related to some
    # specific quantity, and in this case the ordering is what we
    # would expect: the first object is the most recent one!
    ordering = (
        "-upload_date",
        "name",
        "uuid",
    )

    def __str__(self):
        return f"{self.name} ({self.uuid[0:8]})"
