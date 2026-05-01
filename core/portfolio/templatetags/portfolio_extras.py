# portfolio/templatetags/portfolio_extras.py
from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """Découpe une chaîne par rapport à une clé"""
    return value.split(key)