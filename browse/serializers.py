# -*- encoding: utf-8 -*-

import json

from rest_framework import serializers
from django.contrib.auth.models import User, Group
from browse.models import Entity, Quantity, DataFile, FormatSpecification
from django.urls import reverse


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

    def to_representation(self, instance):
        representation = super(FormatSpecificationSerializer, self).to_representation(
            instance
        )
        representation["download_link"] = reverse(
            "format-spec-download-view", kwargs={"pk": instance.uuid}
        )

        return representation


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

    def to_representation(self, instance):
        representation = super(DataFileSerializer, self).to_representation(instance)

        # Convert the string containing the metadata into a proper Python dictionary
        representation["metadata"] = json.loads(instance.metadata)
        representation["download_link"] = reverse(
            "data-file-download-view", kwargs={"pk": instance.uuid}
        )

        return representation
