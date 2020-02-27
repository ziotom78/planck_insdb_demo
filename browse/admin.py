# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import Entity, Quantity, DataFile, FormatSpecification

admin.site.register(Entity)
admin.site.register(Quantity)
admin.site.register(DataFile)
admin.site.register(FormatSpecification)
