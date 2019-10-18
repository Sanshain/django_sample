# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod, abstractproperty

import datetime, time

from django.contrib.auth.models import AbstractUser#, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator

from django.db import models
from django.db.models.signals import post_init                      #сигналы
from django.db.models.signals import pre_save, post_save


from django.dispatch import receiver                                #сигналы

from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from main.utils import Enum
from .extension import MixinModel
# Create your models here.



RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

class State:
    No = '0'
    NOT = '-1'
    Yes = '1'
    EXC = '-0'
    wanted = ''

RELATION_STATUS = [
    (State.No, 'Неизвестный'),                                                          # неподтвержденный
    (State.NOT, 'Не одобренный'),                                                         # отклоненный
    (State.Yes, 'Одобренный'),
    (State.EXC, 'Исключенный'),
]




##FRIEND_TYPE = (
##    ('1', 'Приятель'),
##    ('2', 'Близкий друг'),
##    ('3', 'Родственник')
##)


FRIEND_TYPE = Enum(
    #u'Приятель',
    u'Друг',
    u'Личный друг',                                                                 # приват
    u'Родственник'                                                                  # приват. настраивается
)


##FRIEND_TYPE = {
##    '1' : 'Приятель',
##    '2' : 'Близкий друг',
##    '3' : 'Родственник'
##}

GENDER = (
    ('', 'Не выбран'),
    ('M', 'Муж'),
    ('F', 'Жен'),
)



class Profile(AbstractUser):

    class Meta:
        ordering = ['id']
        verbose_name = u'человека'
        verbose_name_plural = u'Люди'

    City = models.CharField(max_length=90, verbose_name='Город')
    Sex = models.CharField(max_length=1, choices=GENDER, verbose_name='Половина')                               # models.BooleanField(default=True)
    #Age = models.SmallIntegerField(null=True,verbose_name='Возраст')
    Age = models.DateField(null=True,verbose_name='День рождения')

    Image = models.ImageField(upload_to='static/imagination', max_length=100,verbose_name='Ваше изображение')   # height_field=None, width_field=None,

    pals = models.ManyToManyField("self", symmetrical=False, through="Friends", through_fields=('friend', 'by'))



    def __init__(self, *args, **kwargs):

        super(Profile, self).__init__(*args, **kwargs)

        self._meta.get_field('username').validators[0] = ASCIIUsernameValidator(
			message = u'Введите валидное имя. Имя может содержать цифры, буквы лат алфавита и знаки @.+-_'
		)

    def get_absolute_url(self):
		return '/success/'
        # return u'/some_url/%d' % self.id
		# либо https://stackoverflow.com/questions/38840366/no-url-to-redirect-to-either-provide-a-url-or-define-a-get-absolute-url-method
		# return "/people/%i/" % self.id
		# https://docs.djangoproject.com/en/1.11/ref/models/instances/#django.db.models.Model.validate_unique

    def Get_Friends(self, **kwargs):
        #friends = self.pals.filter(Q(bu))
        print kwargs

        if kwargs:
            return friends.filter(**kwargs)

        return friends


class Life(models.Model):
    Leaser = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, related_name='life')
    Image = models.BinaryField()
    Confidence = models.CharField(max_length=50, default='friendship')


@receiver(post_save, sender=Profile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Life.objects.create(Laeser=instance)


@receiver(pre_save, sender = Profile)
def profile_saved(instance, **kwargs):
    """
    print '--------------'
    print instance
    print '--------------'
    print kwargs
    print '--------------'
    """
    pass

"""
@receiver(post_init, sender = Profile)
def logg(instance, **kwargs):
    print 'logggggggggggggggggggg'
"""






# MixinModel
class Friends(models.Model, MixinModel):
    by = models.ForeignKey(Profile, related_name="from_friend")
    friend = models.ForeignKey(Profile, related_name="to_friend")

    #approved = models.NullBooleanField()                                                       #это статус, одобрен/нет или не задан

    approve = models.CharField(max_length=2, choices=RELATION_STATUS, default=State.No)
    date_initiative = models.DateTimeField(default=timezone.now)						        #дата изменения статуса

    Quired_Relation  = models.CharField(max_length=12, choices=FRIEND_TYPE, default='1')        #это запрашиваемый статус
    CurrentRelation = models.CharField(max_length=12, choices=FRIEND_TYPE, default='0')         #это текущий статус ('')

    class Meta:
        unique_together = ('by', 'friend',)                                      #уникальны вместе

    def __unicode__(self):
        return self.by.username + ' with ' + self.friend.username








