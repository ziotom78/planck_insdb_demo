# -*- encoding: utf-8 -*-

# See the Django docs to understand how this works:
# https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/

import json

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def format_json(value):
    try:
        d = json.loads(value)
        return json.dumps(d, indent=4)
    except json.JSONDecodeError:
        pass

    return value
