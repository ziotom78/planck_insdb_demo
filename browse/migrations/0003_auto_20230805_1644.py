# Generated by Django 3.2.20 on 2023-08-05 16:44

import browse.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("browse", "0002_release_json_file"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Account",
        ),
        migrations.AddField(
            model_name="release",
            name="release_document",
            field=models.FileField(
                blank=True,
                help_text="Document accompanying the release (optional)",
                upload_to=browse.models.release_document_directory_path,
                verbose_name="release document",
            ),
        ),
        migrations.AddField(
            model_name="release",
            name="release_document_mime_type",
            field=models.CharField(
                choices=[
                    ("text/plain", "Plain text"),
                    ("text/html", "HTML"),
                    ("application/pdf", "Adobe PDF"),
                    ("text/rtf", "Rich-Text Format (.rtf)"),
                    ("text/markdown", "Markdown"),
                    ("application/x-abiword", "AbiWord document"),
                    ("application/msword", "Microsoft Word (.doc)"),
                    (
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "Microsoft Word (.docx)",
                    ),
                    ("application/vnd.amazon.ebook", "Amazon Kindle eBook"),
                    ("application/epub+zip", "Electronic publication (EPUB)"),
                    (
                        "application/vnd.oasis.opendocument.text",
                        "OpenDocument text document (.odt)",
                    ),
                    (
                        "application/vnd.oasis.opendocument.presentation",
                        "OpenDocument presentation document (.odp)",
                    ),
                    (
                        "application/vnd.oasis.opendocument.spreadsheet",
                        "OpenDocument spreadsheet document (.ods)",
                    ),
                    ("application/vnd.ms-powerpoint", "Microsoft PowerPoint (.ppt)"),
                    (
                        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        "Microsoft PowerPoint (.pptx)",
                    ),
                    ("application/vnd.ms-excel", "Microsoft Excel (.xls)"),
                    (
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        "Microsoft Excel (.xlsx)",
                    ),
                    ("application/octet-stream", "Other (unknown)"),
                ],
                default="text/plain",
                help_text="This specifies the MIME type of the downloadable copy of the release document",
                max_length=256,
                verbose_name="MIME type of the specification document",
            ),
        ),
        migrations.AlterField(
            model_name="datafile",
            name="file_data",
            field=models.FileField(
                blank=True,
                help_text="File contents (when present)",
                upload_to=browse.models.data_file_directory_path,
                verbose_name="file",
            ),
        ),
        migrations.AlterField(
            model_name="datafile",
            name="metadata",
            field=models.TextField(
                blank=True,
                help_text="JSON record containing metadata for the file",
                max_length=32768,
                validators=[browse.models.validate_json],
                verbose_name="JSON-formatted metadata",
            ),
        ),
        migrations.AlterField(
            model_name="datafile",
            name="plot_file",
            field=models.FileField(
                blank=True,
                help_text="Plot of the data in the file (optional)",
                upload_to=browse.models.full_plot_file_path,
                verbose_name="image file",
            ),
        ),
        migrations.AlterField(
            model_name="datafile",
            name="upload_date",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text="Date when the file was added to the database",
                verbose_name="date when the file was uploaded",
            ),
        ),
        migrations.AlterField(
            model_name="release",
            name="json_file",
            field=models.FileField(
                blank=True,
                editable=False,
                help_text="A JSON dump of the release, ready to be downloaded",
                upload_to="",
            ),
        ),
    ]
