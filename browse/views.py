# -*- encoding: utf-8 -*-

# from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from browse.models import Entity, Quantity, DataFile, FormatSpecification

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
