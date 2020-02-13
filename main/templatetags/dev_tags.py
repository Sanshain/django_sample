# -*- coding: utf-8 -*-

from django.conf import settings
from django.template.loader_tags import do_include

from django import template
register = template.Library()

@register.tag('dev_include')
def dev_include(parser, token):

    if not settings.HAML_COMPILE: token.contents = token.contents.replace('.haml','.html')

    return do_include(parser, token)


@register.tag('frag')
def frag_include(parser, token):

    token = 'fragments/{}.{}'.format(token, settings.TEMPLATE_EXTENSION)

    return do_include(parser, token)


@register.tag('unit')
def frag_include(parser, token):

    token = 'components/{}.{}'.format(token, settings.TEMPLATE_EXTENSION)

    return do_include(parser, token)

