# -*- encoding: utf-8 -*-

from collections import OrderedDict
from pathlib import Path
import json
import yaml

import git

from instrumentdb import __version__

from django.utils import timezone
from django.core.management.base import BaseCommand
from browse.models import (
    Entity,
    Quantity,
    DataFile,
    FormatSpecification,
    Release,
    plot_file_directory_path,
)

# File dump is done in chunks; this variable specifies the
# size of one chunk (in bytes)
COPY_CHUNK_SIZE = 1024 * 1024

# This is used as a wrapper to strings that must be quoted in YAML
# output. Consider the following code:
#
#     yaml.dumps({"a": "hello"})
#
# This produces:
#
#     a: hello
#
# Instead, the following code
#
#     yaml.dumps({"a": Quoted("hello")})
#
# produces
#
#     a: "hello"
#
# I find the latter more readable, and it prevents some of the
# problems outlined in this article:
#
#     https://www.arp242.net/yaml-config.html


class Quoted(str):
    pass


# Taken from
# https://stackoverflow.com/questions/5121931/
# /in-python-how-can-you-load-yaml-mappings-as-ordereddicts
def yaml_saner_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _quoted_representer(dumper, data):
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items()
        )

    OrderedDumper.add_representer(Quoted, _quoted_representer)

    # This enables the serialization of OrderedDict objects
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


class Command(BaseCommand):
    help = "Exports the contents of a database into a local directory"
    output_transaction = False
    requires_migrations_checks = True

    def save_attachment(self, relative_path, file_data):
        """Save a file into the specified path under the output folder

        This function is used to save specification documents, data
        files and plot files.

        The parameter "relative_path" specifies the sub-folder *and*
        file name, which is considered relative to self.output_folder
        (set within Command.handle).

        """
        abs_path = self.output_folder / relative_path
        abs_path.parent.mkdir(parents=True, exist_ok=True)

        with file_data.open("rb") as inpf, abs_path.open("wb") as outf:
            while True:
                data = inpf.read(COPY_CHUNK_SIZE)
                if not data:  # end of file reached
                    break
                outf.write(data)

    def dump_entity_tree(self, entities):
        result = []
        for cur_entity in entities:
            # We use a OrderedDict here because otherwise "children" would
            # be the first key in the JSON file, and this would make the
            # file harder to read
            new_element = OrderedDict(
                [("uuid", Quoted(cur_entity.uuid)), ("name", Quoted(cur_entity.name))]
            )

            # Add the "children" key at the bottom of the list of keys
            children = cur_entity.get_children()
            if children:
                # Descend the tree recursively
                new_element["children"] = self.dump_entity_tree(children)

            result.append(new_element)

        return result

    def dump_specifications(self, specs):
        result = []
        for cur_spec in specs:
            cur_entry = OrderedDict(
                [
                    ("uuid", Quoted(cur_spec.uuid)),
                    ("document_ref", Quoted(cur_spec.document_ref)),
                    ("title", Quoted(cur_spec.title)),
                    ("file_mime_type", Quoted(cur_spec.file_mime_type)),
                    ("doc_mime_type", Quoted(cur_spec.doc_mime_type)),
                ]
            )

            if cur_spec.doc_file_name and (not self.no_attachments):
                dest_path = (
                    Path("format_spec") / f"{cur_spec.uuid}_{cur_spec.doc_file_name}"
                )
                cur_entry["file_name"] = Quoted(dest_path)

                self.save_attachment(dest_path, cur_spec.doc_file)

            result.append(cur_entry)

        return result

    def dump_quantities(self, quantities):
        result = []
        for cur_quantity in quantities:
            cur_entry = OrderedDict(
                [
                    ("uuid", Quoted(cur_quantity.uuid)),
                    ("name", Quoted(cur_quantity.name)),
                    ("format_spec", Quoted(cur_quantity.format_spec.uuid)),
                    ("entity", Quoted(cur_quantity.parent_entity.uuid)),
                ]
            )

            result.append(cur_entry)

        return result

    def dump_data_files(self, data_files):
        result = []
        for cur_data_file in data_files:
            cur_entry = OrderedDict(
                [
                    ("uuid", Quoted(cur_data_file.uuid)),
                    ("name", Quoted(cur_data_file.name)),
                    ("upload_date", Quoted(cur_data_file.upload_date)),
                    ("metadata", json.loads(cur_data_file.metadata)),
                    ("quantity", Quoted(cur_data_file.quantity.uuid)),
                    ("spec_version", Quoted(cur_data_file.spec_version)),
                ]
            )

            if cur_data_file.file_data and (not self.no_attachments):
                dest_path = (
                    Path("data_files") / f"{cur_data_file.uuid}_{cur_data_file.name}"
                )
                cur_entry["file_name"] = Quoted(dest_path)

                self.save_attachment(dest_path, cur_data_file.file_data)

            if cur_data_file.plot_file and (not self.no_attachments):
                dest_path = (
                    Path("plot_files")
                    / plot_file_directory_path(cur_data_file, "").name
                )
                cur_entry["plot_file"] = Quoted(dest_path)
                cur_entry["plot_mime_type"] = Quoted(cur_data_file.plot_mime_type)
                self.save_attachment(dest_path, cur_data_file.file_data)

            if cur_data_file.dependencies:
                cur_entry["dependencies"] = [
                    Quoted(x.uuid) for x in cur_data_file.dependencies.all()
                ]

            result.append(cur_entry)

        return result

    def dump_releases(self, releases):
        result = []
        for cur_release in releases:
            cur_entry = OrderedDict(
                [
                    ("tag", Quoted(cur_release.tag)),
                    ("release_date", Quoted(cur_release.rel_date)),
                    ("comment", Quoted(cur_release.comment)),
                    (
                        "data_files",
                        [Quoted(x.uuid) for x in cur_release.data_files.all()],
                    ),
                ]
            )

            result.append(cur_entry)

        return result

    def save_schema(self, output_file_path):
        try:
            this_repo = git.Repo(search_parent_directories=True)
            git_sha = this_repo.head.object.hexsha
        except git.InvalidGitRepositoryError:
            git_sha = "unknown"

        schema = OrderedDict(
            [
                (
                    "instrumentdb",
                    OrderedDict(
                        [
                            ("git_sha", git_sha),
                            ("version", Quoted(__version__)),
                            ("dump_date", timezone.now().isoformat()),
                            (
                                "repository",
                                Quoted("https://github.com/ziotom78/instrumentdb"),
                            ),
                        ]
                    ),
                ),
                ("entities", self.dump_entity_tree(Entity.objects.root_nodes())),
                (
                    "format_specifications",
                    self.dump_specifications(FormatSpecification.objects.all()),
                ),
                ("quantities", self.dump_quantities(Quantity.objects.all())),
                ("data_files", self.dump_data_files(DataFile.objects.all())),
                ("releases", self.dump_releases(Release.objects.all())),
            ]
        )

        with output_file_path.open("w") as outf:
            if output_file_path.suffix == ".yaml":
                yaml_saner_dump(schema, stream=outf)
            else:
                json.dump(schema, outf, indent=2)

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-attachments",
            action="store_true",
            help="Do not save data files, only the JSON file",
        )
        parser.add_argument(
            "--json",
            default=True,
            action="store_true",
            help="Use JSON as the format of the file containing the schema "
            "(always true)",
        )
        parser.add_argument(
            "--yaml",
            action="store_true",
            help="Save a copy of the schema using the YAML format (useful "
            "for legacy codes)",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite anything that is already present in the output path",
        )
        parser.add_argument(
            "output_path",
            help="""
Directory where to store the contents of the database.
If the folder does not exist, it will be created.""",
            type=str,
        )

    def handle(self, *args, **options):
        self.no_attachments = options["no_attachments"]
        self.exist_ok = options["force"]
        self.use_json = options["json"]
        self.use_yaml = options["yaml"]
        self.output_folder = Path(options["output_path"])

        # Create the output directory
        self.output_folder.mkdir(parents=True, exist_ok=self.exist_ok)

        extensions = []
        if self.use_json:
            extensions.append("json")

        if self.use_yaml:
            extensions.append("yaml")

        for cur_ext in extensions:
            self.save_schema(self.output_folder / f"schema.{cur_ext}")
