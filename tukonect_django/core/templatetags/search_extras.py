from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """Template filter to look up a value in a dictionary by key"""
    return dictionary.get(key)
