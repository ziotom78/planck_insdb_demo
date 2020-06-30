# -*- encoding: utf-8 -*-

import mimetypes
from pathlib import Path

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import viewsets

from browse.models import Entity, Quantity, DataFile, FormatSpecification, Release
from browse.serializers import (
    UserSerializer,
    GroupSerializer,
    FormatSpecificationSerializer,
    EntitySerializer,
    QuantitySerializer,
    DataFileSerializer,
    ReleaseSerializer,
)

mimetypes.init()

###########################################################################


def entity_tree_view(request):
    return render(
        request,
        Path("browse") / "entity_list.html",
        {"object_list": Entity.objects.all()},
    )


class EntityView(DetailView):
    model = Entity


###########################################################################


class QuantityListView(ListView):
    model = Quantity


class QuantityView(DetailView):
    model = Quantity


###########################################################################


class DataFileListView(ListView):
    model = DataFile


class DataFileView(DetailView):
    model = DataFile


class FormatSpecificationListView(ListView):
    model = FormatSpecification


class FormatSpecificationDownloadView(View):
    def get(self, request, pk):
        "Allow the user to download a data file"

        cur_object = get_object_or_404(FormatSpecification, pk=pk)
        file_data = cur_object.doc_file
        file_data.open()
        data = file_data.read()
        resp = HttpResponse(data, content_type=cur_object.doc_mime_type)
        resp["Content-Disposition"] = 'attachment; filename="{0}"'.format(
            Path(cur_object.doc_file_name).name
        )
        return resp


class DataFileDownloadView(View):
    def get(self, request, pk):
        "Allow the user to download a data file"

        cur_object = get_object_or_404(DataFile, pk=pk)
        file_data = cur_object.file_data
        file_data.open()
        data = file_data.read()
        resp = HttpResponse(
            data, content_type=cur_object.quantity.format_spec.file_mime_type
        )
        resp["Content-Disposition"] = 'attachment; filename="{0}"'.format(
            Path(cur_object.name).name
        )
        return resp


class DataFilePlotDownloadView(View):
    def get(self, request, pk):
        "Allow the user to download the plot associated with a data file"

        cur_object = get_object_or_404(DataFile, pk=pk)
        plot_file_data = cur_object.plot_file
        plot_file_data.open()
        data = plot_file_data.read()
        resp = HttpResponse(data, content_type=cur_object.plot_mime_type)

        resp["Content-Disposition"] = 'attachment; filename="{name}{ext}"'.format(
            name=Path(cur_object.name).name,
            ext=mimetypes.guess_extension(cur_object.plot_mime_type),
        )
        return resp


###########################################################################


class ReleaseListView(ListView):
    model = Release


class ReleaseView(DetailView):
    model = Release


################################################################################
# REST API


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FormatSpecificationViewSet(viewsets.ModelViewSet):
    queryset = FormatSpecification.objects.all()
    serializer_class = FormatSpecificationSerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class QuantityViewSet(viewsets.ModelViewSet):
    queryset = Quantity.objects.all()
    serializer_class = QuantitySerializer


class DataFileViewSet(viewsets.ModelViewSet):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer


class ReleaseViewSet(viewsets.ModelViewSet):
    # Enable dots to be used in release tag names. See
    # https://stackoverflow.com/questions/27963899/django-rest-framework-using-dot-in-url
    lookup_value_regex = "[\w.]+"
    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer


################################################################################


def release_view(request, rel_name, reference, browse_view=False):
    # If browse_view is True, redirect to browse/data_files/uuid
    # If browse_view is False, redirect to api/data_files/uuid

    release = get_object_or_404(Release, tag=rel_name)

    # The "reference" here is the part of the URL that includes the
    # list of entities and the quantity. For instance, if "reference"
    # is "mft/detectors/det0a/noise_properties", this is the meaning
    # of its parts:
    #
    #     mft / detectors / det0a / noise_properties
    #     |---------------------|   |--------------|
    #               ^                      ^
    #               |                      |
    #      sequence of entities         quantity

    url_components = reference.split("/")
    quantity_name = url_components[-1]

    cur_queryset = get_object_or_404(Entity, name=url_components[0])
    for comp in url_components[1:-1]:
        cur_queryset = get_object_or_404(cur_queryset.get_children(), name=comp)

    quantity = get_object_or_404(cur_queryset.quantities, name=quantity_name)
    data_file = get_object_or_404(quantity.data_files, release_tags__tag=release.tag)

    if browse_view:
        return redirect("data-file-view", data_file.uuid)
    else:
        return redirect("datafile-detail", data_file.uuid)


def api_release_view(request, rel_name, reference):
    return release_view(request, rel_name, reference, browse_view=False)


def browse_release_view(request, rel_name, reference):
    return release_view(request, rel_name, reference, browse_view=True)
