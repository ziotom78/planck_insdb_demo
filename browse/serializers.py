# -*- encoding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from browse.models import Entity, Quantity, DataFile, FormatSpecification


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class FormatSpecificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FormatSpecification
        fields = [
            "uuid",
            "document_ref",
            "title",
            "doc_file_name",
            "doc_mime_type",
            "file_mime_type",
        ]


class SubEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = [
            "uuid",
            "name",
        ]


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    children = SubEntitySerializer(many=True, required=False)

    class Meta:
        model = Entity
        fields = [
            "uuid",
            "name",
            "parent",
            "children",
            "quantities",
        ]


class QuantitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quantity
        fields = [
            "uuid",
            "name",
            "format_spec",
            "parent_entity",
            "data_files",
        ]


class DataFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataFile
        fields = [
            "uuid",
            "name",
            "upload_date",
            "metadata",
            "quantity",
            "spec_version",
            "dependencies",
            "plot_mime_type",
            "comment",
        ]
