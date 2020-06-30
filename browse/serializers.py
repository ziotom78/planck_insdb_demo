# -*- encoding: utf-8 -*-

import json

from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.models import User, Group
from browse.models import Entity, Quantity, DataFile, FormatSpecification, Release


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class FormatSpecificationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="formatspecification-detail", read_only=True
    )

    class Meta:
        model = FormatSpecification
        fields = [
            "uuid",
            "url",
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
            "format-spec-download-view",
            kwargs={"pk": instance.uuid},
            request=self.context["request"],
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
    url = serializers.HyperlinkedIdentityField(
        view_name="entity-detail", read_only=True
    )

    class Meta:
        model = Entity
        fields = [
            "uuid",
            "url",
            "name",
            "parent",
            "children",
            "quantities",
        ]


class QuantitySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="quantity-detail", read_only=True
    )

    class Meta:
        model = Quantity
        fields = [
            "uuid",
            "url",
            "name",
            "format_spec",
            "parent_entity",
            "data_files",
        ]


class DataFileSerializer(serializers.HyperlinkedModelSerializer):
    release_tags = serializers.HyperlinkedRelatedField(
        view_name="release-detail", many=True, queryset=Release.objects.all(),
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="datafile-detail", read_only=True
    )

    class Meta:
        model = DataFile
        fields = [
            "uuid",
            "url",
            "name",
            "upload_date",
            "metadata",
            "quantity",
            "spec_version",
            "dependencies",
            "plot_mime_type",
            "comment",
            "release_tags",
        ]

    def to_representation(self, instance):
        representation = super(DataFileSerializer, self).to_representation(instance)

        # Convert the string containing the metadata into a proper Python dictionary
        representation["metadata"] = json.loads(instance.metadata)
        representation["download_link"] = reverse(
            "data-file-download-view",
            kwargs={"pk": instance.uuid},
            request=self.context["request"],
        )
        representation["plot_download_link"] = reverse(
            "data-file-plot-view",
            kwargs={"pk": instance.uuid},
            request=self.context["request"],
        )

        return representation

    def to_internal_value(self, data):
        value = super(DataFileSerializer, self).to_internal_value(data)

        value["metadata"] = json.dumps(data, indent=2)

        return value


class ReleaseSerializer(serializers.HyperlinkedModelSerializer):
    data_files = serializers.HyperlinkedRelatedField(
        view_name="datafile-detail", many=True, queryset=DataFile.objects.all(),
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="release-detail", read_only=True
    )

    class Meta:
        model = Release
        fields = [
            "tag",
            "url",
            "rel_date",
            "comments",
            "data_files",
        ]
        ordering = ["-rel_date"]
