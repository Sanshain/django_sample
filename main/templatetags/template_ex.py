# -*- coding: utf-8 -*-
##from ...hello import settings

from django.conf import settings

from django.contrib.staticfiles.templatetags.staticfiles import static
from django import template
register = template.Library()


@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name


@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural


"""
\1й арг - модель
\2й арг - название поля
"""
@register.filter
def field_name(obj, field):
    #verbose_name для поля
    return obj._meta.get_field(field).verbose_name

@register.filter
def fields(obj):
    #print obj._meta.get_fields().__class__
    return obj._meta.get_fields()













#utils:

import os

    ##    values = list(obj._meta.get_fields())
    ##    if includ:
    ##        values = set(values).intersection(includ)
    ##        return values

#fields = GetFields(Pofile)
#Get_Templates(settings.TEMPLATE_DIR, fields)

def GetFields(model, exclud = None, includ = None):

    values = []
    if includ:
        for field in obj._meta.get_fields():
            if field in includ:
                values.append(field_view(field))
        return values
    elif exclud:
        for field in obj._meta.get_fields():
            if field not in exclud:
                values.append(field_view(field))
    else:
        for field in obj._meta.get_fields():
            values.append(field_view(field))

    return values

def GetFields_as_dict(model, exclud = None, includ = None):

    values = {}
    if includ:
        for field in obj._meta.get_fields():
            if field in includ:
                values.update(field, field_view(field))
        return values
    elif exclud:
        for field in obj._meta.get_fields():
            if field not in exclud:
                values.update(field, field_view(field))
    else:
        for field in obj._meta.get_fields():
            values.update(field, field_view(field))

    return values

def Get_Templates(directory, values):
    files = os.listdir(directory)
    templs = filter(lambda x: x.endswith('.teml'), files)

    if (type(values) == type([])):
        for temp in templs:
            TemlToTemp(temp, values)
    if (type(values) == type({})):
        for temp in templs:
            TemlToTemp_fromDict(temp, values)

def TemlToTemp_fromDict(directory, values):
    with open(filename, '+') as fle:                                                    #+
        data = fle.read()
        for key, val in values:
            data = data.replace('{{# %s #}}'%key, val)
        fle.write(data)


def TemlToTemp(filename, values):
    i=0
    with open(filename, '+') as fle:                                                    #+
        data = fle.read()
        for val in values:
            data = data.replace('{{# %s #}}'%i, val)
            i+=1
        fle.write(data)                                                                 #fle.seek(0)

"""

"""
def field_view(field):
    str = "<p class='atr'> {{ profile|field_name:'%s' }}: <span class='ab'> {{ profile.%s }}</span> </p>"%field%field
    return str



@register.simple_tag
def includes(filename):
    f = os.path.join(settings.BASE_DIR, 'main/templates', filename).replace('\\','/')

    return f

