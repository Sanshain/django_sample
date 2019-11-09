# -*- coding: utf-8 -*-

from django.conf import settings

from django.db import models
from django.db.models import Count

from django.utils import timezone
from main.models import Profile
from django.db.models import OuterRef, Subquery                                     # для подзапросов

import datetime

from ..utils.utime import present_time


class Dialogue_Partakers(models.Model):
    Profile = models.ForeignKey(Profile, related_name='talks')
    Dialogue = models.ForeignKey('Dialogue', related_name='talkers')
##    Time = models.DateTimeField()
##    Last = models.ForeignKey('Message', null=True)
    Last = models.IntegerField()                                                # последнее сообщение в диал, не obsolete пока

class Dialogue(models.Model):
##    class Meta:
##        ordering = ('messages__id', )

    Partakers = models.ManyToManyField(Profile, related_name='dialogs', through="Dialogue_Partakers")
#    Partakers = models.JSONField(Profile:Time)

    @staticmethod
    def get_private_Dialog(buddy_id, self_id):
        """
        Получаю либо создаю, если такого нет, диалог между двумя юзерами,
        а так же аннотирует картинку собеседника в talker_image этого диалога
        """
        partakers = [buddy_id, self_id]

        buddy = Profile.objects.get(id=buddy_id)
        me = Profile.objects.get(id=self_id)

        dialogs = Dialogue.objects.annotate(cnt=Count('Partakers')).filter(cnt=len(partakers))

        Image = Subquery(Profile.objects.filter(dialogs=OuterRef('id')).filter(id=buddy_id).values('Image')[:1])
        dialogs = dialogs.annotate(talker_image=Image)                            # settings.MEDIA_URL +

        dialog, created = dialogs.filter(Partakers__id=self_id).get_or_create(Partakers__id=buddy_id)

        if created:                                                                                             ## dialog.Partakers = partakers - если нет пром модели
            Dialogue_Partakers.objects.bulk_create([                                                             ## не будет вызван save и сигналы
                Dialogue_Partakers(Dialogue=dialog, Profile_id=self_id),
                Dialogue_Partakers(Dialogue=dialog, Profile_id=buddy_id)
            ])

        return dialog

    #obcolete
    @staticmethod
    def get_for_buddys(sender_id, recipient_id):

##        dialog, created = Dialogue.objects.get_or_create(Partakers__id=buddy_id)          - самый первый рабочий способ
##        print dialog
##
##        if created:
##            buddy = Profile.objects.get(id=buddy_id)
##            dialog.Partakers = [buddy, self.request.user]


##        recipient = Profile.objects.get(id=recipient_id)

##        dialog = Dialogue.objects.get_or_create(Partakers=[recipient_id,self.request.user.id]) - ошибка

##        dialog = Dialogue.objects.get(Partakers__id=recipient_id)                                  - работает для одного

##        partakers = chain(Profile.objects.none(),[Profile.objects.get(id=recipient_id),self.request.user])
##        dialog = Dialogue.objects.get(Partakers__in=partakers)                                  ## - находит все диалоги с этими собеседниками

##        partakers = chain(Profile.objects.none(),[Profile.objects.get(id=buddy_id),self.request.user])    - работает для 2, но в теории только если такой диалог 1.
##        dialogs = Dialogue.objects.filter(Partakers__in=partakers).annotate(num_partekers=Count('Partakers'))
##        dialogs = [dialog for dialog in dialogs if dialog.num_partekers == 2]
##
##        print dialogs

##        partakers = chain(Profile.objects.none(),[Profile.objects.get(id=buddy_id),self.request.user])  - более успешный предыдущий вариант
##        dialogs = Dialogue.objects.filter(Partakers__id__in=[buddy_id,self.request.user.id]).annotate(num_partekers=Count('Partakers'))
##        print len(dialogs)
##        for d in dialogs:
##            print u":%s"%d.num_partekers
##        dialogs = [dialog for dialog in dialogs if dialog.num_partekers == 2]
##        dialog = dialogs.pop()
##        print len(dialogs)
##        print dialog.id

##        dialog = self.request.user.dialogs.filter(Partakers__id=buddy_id)             - не возвращает ничего, см сам запрос - нереальный. Надо заджйнить два раза
##        print dialog

##        dialog = Dialogue.objects.filter(Partakers__id=recipient_id).get(Partakers=self.request.user) # получил, но если есть еще беседы, где они пересекаются, то....
##        dialog = Dialogue.objects.filter(Q(Partakers__id=recipient_id), Q(Partakers__id=self.request.user.id)) # ничего не возвращает, хотя должен
##        dialog = self.request.user.dialogs.filter(Partakers=recipient)                    # то же, что и Q

##        dialogs = Dialogue.objects.filter(Partakers__id=recipient_id).filter(Partakers__id=sender_id) - ничего не вернет по count
##        dialogs = dialogs.annotate(num_partekers=Count('Partakers'))
##        dialogs = [dialog for dialog in dialogs if dialog.num_partekers == 2]
##        dialog = dialogs.pop()

        partakers = [recipient_id, sender_id]
        dialogs = Dialogue.objects.annotate(cnt=Count('Partakers')).filter(cnt=len(partakers))
        dialogs = dialogs.filter(Partakers__id=recipient_id).filter(Partakers__id=sender_id)

        print len(dialogs)

        dialog = list(dialogs).pop() if len(dialogs) else None

        return dialog


class Message(models.Model):
    Sender = models.ForeignKey(Profile, related_name='msgs', related_query_name="msgs")

    Time = models.DateTimeField(default=present_time)                            #  default=timezone.now # default=datetime.datetime.now
    Content = models.TextField()

    Target = models.ForeignKey(Dialogue, related_name='messages', related_query_name="messages")      # это так же может быть Profile, тогда будет работать быстрее


