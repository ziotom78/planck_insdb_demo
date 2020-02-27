# -*- encoding: utf-8 -*-

from pathlib import Path
import json
import sys
import yaml

from django.core.files import File
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand, CommandError
from browse.models import Entity, Quantity, DataFile, FormatSpecification


class Command(BaseCommand):
    help = "Load records into the database from a YAML file"
    output_transaction = True
    requires_migrations_checks = True

    def create_entities(self, entities, parent=None, nest_level=0):
        for entity_dict in entities:
            cur_entity_name = entity_dict.get("name")
            uuid = entity_dict.get("uuid")

            spaces = " " * (nest_level * 2)
            if uuid:
                self.stdout.write(spaces + f"Entity {cur_entity_name} ({uuid[0:6]})")
            else:
                self.stdout.write(spaces + f"Entity {cur_entity_name}")

            if not self.dry_run:
                cur_entity = Entity.objects.create(
                    uuid=uuid, name=cur_entity_name, parent=parent
                )
            else:
                cur_entity = cur_entity_name

            # Recursively create children
            self.create_entities(
                entity_dict.get("children", []),
                parent=cur_entity,
                nest_level=nest_level + 1,
            )

            if not self.dry_run:
                cur_entity.save()

    def create_format_specifications(self, specs):
        for spec_dict in specs:
            uuid = spec_dict.get("uuid")
            document_ref = spec_dict.get("document_ref")
            uuid = spec_dict.get("uuid")
            doc_file_name = spec_dict.get("doc_file")

            if doc_file_name:
                file_path = self.attachment_source_path / doc_file_name
                fp = open(file_path)
                doc_file = File(fp, "r")
            else:
                file_path = "<no file>"
                fp = None
                doc_file = None

            if uuid:
                self.stdout.write(
                    f'Format specification "{document_ref}" ({uuid[0:6]}, {file_path})'
                )
            else:
                self.stdout.write(
                    f'Format specification "{document_ref}" ({file_path})'
                )

            if not self.dry_run:
                format_spec = FormatSpecification.objects.create(
                    uuid=uuid,
                    document_ref=document_ref,
                    title=spec_dict.get("title", ""),
                    doc_file=doc_file,
                    doc_file_name=doc_file_name,
                    doc_mime_type=spec_dict.get("doc_mime_type", ""),
                    file_mime_type=spec_dict.get("file_mime_type", ""),
                )

                format_spec.save()

            if fp:
                fp.close()

    def create_quantities(self, quantities):
        for quantity_dict in quantities:
            name = quantity_dict.get("name")
            uuid = quantity_dict.get("uuid")

            if uuid:
                self.stdout.write(f"Quantity {name} ({uuid[0:6]})")
            else:
                self.stdout.write(f"Quantity {name}")

            if self.dry_run:
                continue

            parent_uuid = quantity_dict.get("entity")
            if not parent_uuid:
                raise CommandError(f"expected entity for quantity {name}")

            try:
                parent_entity = Entity.objects.get(uuid=parent_uuid)
            except Entity.DoesNotExist:
                raise CommandError(
                    f"parent {parent_uuid[0:6]} for {name} "
                    f"({uuid[0:6]}) does not exist"
                )

            format_spec_ref = quantity_dict.get("format_spec")
            format_spec = None
            if format_spec_ref:
                try:
                    format_spec = FormatSpecification.objects.get(uuid=format_spec_ref)
                except FormatSpecification.DoesNotExist:
                    self.stderr.write(
                        f"Error, format specification {format_spec_ref} "
                        f"for quantity {name} ({uuid[0:6]}) does not exist"
                    )

            quantity = Quantity.objects.create(
                uuid=uuid,
                name=name,
                format_spec=format_spec,
                parent_entity=parent_entity,
            )

            quantity.save()

    def create_data_files(self, data_files):
        for data_file_dict in data_files:
            name = data_file_dict.get("name")
            uuid = data_file_dict.get("uuid")
            metadata = json.dumps(data_file_dict.get("metadata", {}))
            filename = data_file_dict.get("file_data")
            plot_filename = data_file_dict.get("plot_file")
            dependencies = data_file_dict.get("dependencies", [])

            try:
                upload_date = make_aware(
                    parse_datetime(data_file_dict.get("upload_date"))
                )
            except ValueError:
                raise CommandError(
                    f"invalid upload date for data file {name} ({uuid[0:6]})"
                )

            if not upload_date:
                raise CommandError(
                    f"no upload date specified for data file {name} ({uuid[0:6]})"
                )

            if filename:
                fp = open(self.attachment_source_path / filename)
                file_data = File(fp, "r")
            else:
                file_data = None

            if plot_filename:
                plot_fp = open(self.attachment_source_path / plot_filename)
                plot_file = File(fp, "r")
            else:
                plot_fp = None
                plot_file = None

            if uuid:
                self.stdout.write(f'Data file "{name}" ({uuid[0:6]}, {filename})')
            else:
                self.stdout.write(f'Data file "{name}" ({filename})')

            for cur_dep in dependencies:
                self.stdout.write(f"  Depends on {cur_dep[0:6]}")

            if self.dry_run:
                continue

            parent_uuid = data_file_dict.get("quantity", "")
            parent = Quantity.objects.get(uuid=parent_uuid)

            cur_data_file = DataFile.objects.create(
                uuid=uuid,
                name=name,
                upload_date=upload_date,
                metadata=metadata,
                file_data=file_data,
                quantity=parent,
                spec_version=data_file_dict.get("spec_version"),
                plot_file=plot_file,
                plot_mime_type=data_file_dict.get("plot_mime_type"),
            )

            for cur_dep in dependencies:
                reference = DataFile.objects.get(uuid=cur_dep)
                cur_data_file.dependencies.add(reference)

            cur_data_file.save()

            if fp:
                fp.close()
            if plot_fp:
                plot_fp.close()

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not execute any action on the database (useful for testing)",
        )
        parser.add_argument(
            "--json",
            action="store_true",
            help="Read the schema from a JSON file instead of a YAML file",
        )
        parser.add_argument(
            "schema_file",
            nargs="+",
            help="""
YAML/JSON file containing the specification of the records to be imported
int the database. All the attachments (data files, specification documents,
etc.) will be looked in the directory where this file resides.
""",
            type=str,
        )

    def handle(self, *args, **options):
        self.dry_run = options["dry_run"]
        self.use_json = options["json"]

        for curfile in options["schema_file"]:
            schema_filename = Path(curfile)

            # Retrieve every attachment from the same path where the
            # YAML file is
            self.attachment_source_path = schema_filename.parent

            with open(schema_filename, "rt") as inpf:
                if self.use_json:
                    schema = json.load(inpf)
                else:
                    schema = yaml.safe_load(inpf)

            self.create_entities(schema.get("entities", []))
            self.create_format_specifications(schema.get("format_specifications", []))
            self.create_quantities(schema.get("quantities", []))
            self.create_data_files(schema.get("data_files", []))
