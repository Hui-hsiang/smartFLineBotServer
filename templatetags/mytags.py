import re
from django import template

register = template.Library()

@register.filter(name='thcut')
def thcut(value):
    s = '%.2f' % (value)
    return re.sub(r"(\d)(?=(\d\d\d)+(?!\d))", r"\1,", s)

@register.filter(name='strThcut')
def strThcut(value):
    s = '%s' % (value)
    return re.sub(r"(\d)(?=(\d\d\d)+(?!\d))", r"\1,", s)

