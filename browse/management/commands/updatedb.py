# -*- encoding: utf-8 -*-
import time
from pathlib import Path
import json
from uuid import UUID

from django.core.files import File
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from django.core.management.base import BaseCommand, CommandError
from browse.models import (
    Entity,
    Quantity,
    DataFile,
    FormatSpecification,
    Release,
    update_release_file_dumps,
)


class Command(BaseCommand):
    help = "Update the internal status of the DB"
    output_transaction = True
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="""Force the rebuild of the JSON files for *all* releases,
            even if they already exist""",
        )

    def handle(self, *args, **options):
        force_flag = options["force"]

        print("Going to update the internal status of the DB…")
        start_time = time.perf_counter()
        update_release_file_dumps(force=force_flag)
        end_time = time.perf_counter()
        print("The update has been completed in {:.1f} s".format(end_time - start_time))
