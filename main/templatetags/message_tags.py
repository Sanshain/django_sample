# -*- coding: utf-8 -*-

from django.conf import settings


from django.utils.html import escape

from django import template
register = template.Library()



@register.simple_tag
def flag(content):
    return chr(28)



@register.filter()
def as_media(content):
    if content.startswith(chr(28)):
        return '<img src="{}" />'.format(content.lstrip())
    else:
        return escape(content)



@register.simple_tag
def present(content):
    if content.startswith(chr(28)):
        return '<img src="{}" />'.format(content.lstrip())
    else:
        return content

