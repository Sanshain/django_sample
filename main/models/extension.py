# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod, abstractproperty

import datetime, time

from django.contrib.auth.models import AbstractUser#, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator

from django.db import models
from django.db.models.signals import post_init
from django.db.models.signals import pre_save


from django.dispatch import receiver

from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from main.utils import Enum




class MixinModel(object):

    """
    насколько помню, не работает при миграциях
    """
    @classmethod
    def All(cls):
        return cls.objects.all()

    @classmethod
    def Find(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs)



class DjangoInterface(models.Model):

    def save(self, *args, **kwargs):
        #сделать проверку на название: если первая буква I и вторая - заглавная, значит - это интерфейс и вызываем исключение

        if type(self) is Note: raise Exception(u'INote является абстрактным объектом')
        else: super(Note, self).save(args, kwargs)