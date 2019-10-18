# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod, abstractproperty

import datetime, time

from django.contrib.auth.models import AbstractUser#, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator

from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from django.db.models.signals import post_init
from django.db.models.signals import pre_save


from django.dispatch import receiver

from django.urls import reverse
from django.utils import timezone

from ..utils import Enum
from .users import Profile

class INote(models.Model):                                                           #INote
    ##  абстрактный класс
    #__metaclass__= ABCMeta

    class Meta:

        ordering = ['Time']
        verbose_name = u'Запись'
        verbose_name_plural = u'записи'


    Content = models.TextField(verbose_name=u'содержание')
    Time = models.DateTimeField(auto_now=True, verbose_name=u'Время')
    From = models.ForeignKey(Profile, related_name = '%(class)s')                   #, related_name='Notes' - нельзя, т.к. в дочерних не сможем переопределить и будет ошибка доступа

    def __unicode__(self):
        #date = u'от {}'.format(self.Time.strftime('%d.%m.%Y %H:%M'))
        when = "%H:%M" if self.Time.day == datetime.date.today().day else "%d.%m.%Y"
        return u'%s от %s' % (u'Запись ', self.Time.strftime(when))                 #self.From


    def save(self, *args, **kwargs):

        #сделать проверку на название: если первая буква I и вторая - заглавная, значит - это интерфейс и вызываем исключение
        if type(self) is INote: raise Exception(u'INote является абстрактным объектом')
        else: super(INote, self).save(args, kwargs)


class Comment(INote):
    class Meta:

        verbose_name = u'Комментарий'
        verbose_name_plural = u'комментарий'

    Target = models.ForeignKey(INote, related_name=u'comments', verbose_name=u'К чему')      #Article, Comment - но как исключить Note?

class Article(INote):
    class Meta:

        verbose_name = u'Заметка'
        verbose_name_plural = u'заметка'

    Title = models.CharField(max_length=100, verbose_name=u'Заголовок', blank=True)
    #Category = models.CharField(max_length=100, verbose_name=u'Категория')
    Category = models.ManyToManyField('Mark', verbose_name=u'Категория', related_name='Articles')

    def get_absolute_url(self):
		return reverse('Me')


class Mark(models.Model):                                                           #изменить на Label

    class Meta:

        verbose_name = u'категорию'
        verbose_name_plural = u'Метка'

    #Parent = models.ForeignKey('Mark', related_name='childs')                       #по идее должен подддерживать null
    Value = models.CharField(max_length=50, verbose_name=u'Название')

    def __unicode__(self):

        return self.Value




class Raiting(models.Model):

    class Meta:
        ordering = ['Time']
        verbose_name = u'рейтинг'
        verbose_name_plural = u'Отданный рейтинг'

    From = models.ForeignKey(Profile, related_name='passed_Marks')
    Target = models.ForeignKey(INote, related_name='gained_Marks', verbose_name=u'Запись')
    Time = models.DateTimeField(auto_now=True)                                               #auto_now и auto_now_add скрывает поле в админке помимо всего/ меняется при редактировании
    Value = models.SmallIntegerField(validators=[MinValueValidator(-16), MaxValueValidator(16)] , verbose_name=u'Оценка')

    def __unicode__(self):

        span = timezone.now() - self.Time                                                       # datetime.datetime.now() почему-то не работал, почему не понял

        #print self.Time
        rez = u'%s %s дней назад' % (u'Like ',span.days if span.days < 366 else span.days/366)

        if span.days > 0:
            return rez

        hours = span.total_seconds()//3600

        if hours > 0:
            return u"Поставлена %i часов назад" % (span.total_seconds()//3600)

        else:
            return u"Только что"

        return