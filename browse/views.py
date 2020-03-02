# -*- encoding: utf-8 -*-

from pathlib import Path

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets

from browse.models import Entity, Quantity, DataFile, FormatSpecification
from browse.serializers import (
    UserSerializer,
    GroupSerializer,
    FormatSpecificationSerializer,
    EntitySerializer,
    QuantitySerializer,
    DataFileSerializer,
)

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
        resp["Content-Disposition"] = 'attachment; filename="{0}"'.format(
            Path(cur_object.name).name
        )
        return resp


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
