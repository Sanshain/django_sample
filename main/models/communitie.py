# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Count

from django.utils import timezone
from main.models import Profile

import datetime

from ..utils.utime import present_time



class Community(models.Model):
    Author = models.ForeignKey(Profile)
    member = models.ManyToManyField(Profile, limit_choices_to={'is_active':True})
    title = models.CharField(max_length=50)
    definition = models.TextField(verbose_name='Описание')
    logo = models.ImageField(width_field=300, height_field=400,blank=False)


