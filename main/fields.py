#-------------------------------------------------------------------------------
# Name:        fields.py
# Purpose:
#
# Author:      комп
#
# Created:     17.02.2019
# Copyright:   (c) комп 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#http://qaru.site/questions/54820/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model

from django.db import models

class IntegerRangeField(models.IntegerField):

    def __init__(self,verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):

        self.min_value = min_value
        self.max_value = max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):

        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)

        return super(IntegerRangeField, self).formfield(**defaults)



class EmptyField(models.Field):
    """
    Заглушка для Field, которая не должна сохраняться в базу, но должна имитировать Field в формах
    """
    IsEmpty = True

    def __str__(self):
        return 'EmptyField'
