# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def key_exists(dict_obj, key):
    return key in dict_obj

@register.filter
def item(dict_obj, key):
    return dict_obj.get(key, None)
