# -*- encoding: utf-8 -*-

# from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User, Group

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


class EntityListView(ListView):
    model = Entity


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


class FormatSpecificationView(DetailView):
    model = FormatSpecification


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
