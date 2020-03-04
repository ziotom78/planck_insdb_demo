# -*- encoding: utf-8 -*-

from pathlib import Path
from django.core.management import call_command
from django.test import TestCase
from browse.models import Entity, FormatSpecification, Quantity, DataFile, Release


class TestNestedYamlIO(TestCase):
    def test_import_nested_yaml(self):
        input_file = Path(__file__).parent / ".." / "examples" / "schema1.yaml"
        call_command("importyaml", input_file)
        self.assertEqual(len(Entity.objects.all()), 12)
        self.assertEqual(len(FormatSpecification.objects.all()), 3)
        self.assertEqual(len(Quantity.objects.all()), 12)
        self.assertEqual(len(DataFile.objects.all()), 3)
        self.assertEqual(len(Release.objects.all()), 1)


class TestPlainYamlIO(TestCase):
    def test_import_plain_yaml(self):
        input_file = Path(__file__).parent / ".." / "examples" / "schema2.yaml"
        call_command("importyaml", input_file)
        self.assertEqual(len(Entity.objects.all()), 12)
        self.assertEqual(len(FormatSpecification.objects.all()), 3)
        self.assertEqual(len(Quantity.objects.all()), 12)
        self.assertEqual(len(DataFile.objects.all()), 3)
        self.assertEqual(len(Release.objects.all()), 1)
