# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import chain
import json
import os

# для процедурного стиля:

from django.shortcuts import render						# для страниц, или ниже:
from django.template.response import TemplateResponse 	# для страниц 		https://stackoverflow.com/questions/38838601/django-templateresponse-vs-render
from django.http import HttpResponse, JsonResponse

from django.core import serializers
from django.forms.models import model_to_dict


# для cbv-стиля:
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView               # для страниц
from django.shortcuts import redirect														              # для переадресации псле валидации

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import F, Q
from django.db.models import Count, Min
from django.db.models import Max, Sum, Case, When
from django.db.models import Value, IntegerField
from django.db.models import OuterRef, Subquery, Prefetch
from django.http import HttpResponseRedirect    											              # для AJAX
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string

# main
from main.models import Profile, Friends, State
from main.models.messages import Dialogue, Message, Dialogue_Partakers
from main.views.Mixins import CSSMixin
from ..utils.utime import present_time

if settings.DEBUG:
    from datetime import timedelta, datetime
    import time
    import timeit
    import traceback


@method_decorator(login_required, name='dispatch')
class Dialogs(CSSMixin, ListView):
    model = Dialogue
    template_name = "dialogue_list.html"				                       	    # по умолчанию main/dialogue_list.html
    context_object_name = 'dialogs'	    						                    # object_list by default

    def get_context_data(self, **kwargs):
        context = super(Dialogs, self).get_context_data(**kwargs)
        context['header'] = self.request.user.username

        return context

    def get_queryset(self):

##        qs = super(Dialogs, self).get_queryset()
##        qs = qs.filter(Partakers__in=[self.request.user]).annotate(last=Max('messages__id'))    #.filter(last__gt=0)
##        qs = qs.order_by('-last')

        #это должно быть быстрее, тк будет содержать в предзапросе значение каждого последнего сооб
        lastMessage = Subquery(Message.objects.filter(Target=OuterRef('id')).order_by('-id').values('Content')[:1])
        qs = Dialogue.objects.filter(Partakers__in=[self.request.user]).annotate(lastMess=lastMessage)
        qs = qs.annotate(time=Max('messages__Time')).order_by('-time')

##        qs = qs.annotate(time=Max('messages__Time')).annotate(Sender=Max('messages__Sender__username')).order_by('-time')

##        не то, т.к. неверный результат
##        qs = qs.annotate(SenderImg=Max('messages__Sender__Image'), SenderName=Max('messages__Sender__username')).order_by('-time')

##       на 90мс дольше, т.к. один лишний запрос
##        MessageSender = Subquery(Profile.objects.filter(msgs=OuterRef('id')).order_by('-id').values('Image')[:1])
##        qs = qs.prefetch_related(Prefetch('messages', queryset=Message.objects.annotate(sender_img=MessageSender).select_related('Target'), to_attr='mss'))


        #получаем картинку
        MessageSender = Subquery(Profile.objects.filter(msgs=OuterRef('id')).order_by('-id').values('Image')[:1])
        lastMessageSender = Subquery(Message.objects.filter(Target=OuterRef('id')).annotate(the_sender=MessageSender).order_by('-id').values('the_sender')[:1])
        qs = qs.annotate(SenderImg=lastMessageSender)

        #как взять из промежуточной таблицы значение Time - время последнего посещения диалога
##        myLastTime = Dialogue_Partakers.objects.filter(Profile_id=self.request.user.id).filter(Dialogue=OuterRef('id')).values('Time')[:1]
##        qs = (
##            Dialog
##            .objects
##            .filter(Partakers__in=[self.request.user])
##            .annotate(visit=Subquery(myLastTime))
##            .annotate(unread=Sum(
##                Case(
##                    When(messages__Time__gt=F('visit'), then=Value(1)),
##                    default=Value(0),
##                    output_field=IntegerField(),
##                )
##            ))
##        )

        LastReaded = Dialogue_Partakers.objects.filter(Profile_id=self.request.user.id).filter(Dialogue=OuterRef('id')).values('Last')[:1]

        qs = qs.annotate(visit=Subquery(LastReaded))        #.annotate(sender_id=Min('messages__Sender__id'))

        qs = qs.annotate(unread=Sum(
            Case(
                When(Q(messages__id__gt=F('visit')) & ~Q( messages__Sender = self.request.user), then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ))

##        qs = qs.annotate(count=Count('messages'))

##        print [q.last for q in qs]
##        mess = Message.objects.filter(id__in=[q.last for q in qs])                              # опять вопрос к сортировке
##        print mess.count()
##        ivar=0
##        for q in qs:
##            print q.sender_id
##            if q.last:
##                q.message = mess[ivar]
##                ivar+=1
##        print qs[0].messages.count()
##        print qs[0].messages__count

        return qs


    def post(self, *args, **kwargs):

        detail = self.request.POST.get('detail', None)

        tag_ren = {}

        if detail:

            template_snippet = os.path.join('fragments','_dialogue_list.html')
            tag_ren['main'] = render_to_string(template_snippet, context={
                'object_list' : self.get_queryset(),
                'MEDIA_URL' : settings.MEDIA_URL
            })

            styles = self.get_default_style()['links']
            if len(styles): tag_ren['dynamic_link'] = styles[0]

            return JsonResponse(tag_ren, safe=False)

        else:

            return JsonResponse(tag_ren)





@method_decorator(login_required, name='dispatch')
class Dialog(ListView):
    model = Message
    # template_name =           							                       	# по умолчанию main/dialog_list.html
    context_object_name = 'messages'							                    # object_list by default

    """
    сохраняет в Dialogue:Partaker в поле `Last` id последнего прочитанного сообщения в Dialogue текущим Partaker
    - занимает примерно 110 мс

    [вот здесь записываем в dialogue_Partakers значение Time - время последнего прочтения тек пользователем сообщений в диалоге]
    """
    def _update_presence(self, dialog, last=None):

        monolog = Dialogue_Partakers.objects.annotate(last=Max('Dialogue__messages__id')).get(Dialogue_id=dialog,Profile_id=self.request.user.id)
        # получаем id последнего сообщения в этом диалоге и если не передано заведомо другое, то назначаем его:
        if monolog:
            monolog.Last = monolog.last or last
            monolog.save()
            return False                                                     # сохраняем последнего просмотра сообщений текущего пользователя
        else:
            return True

##        print 'monolog.last: ' + str(monolog.last)



    def get_context_data(self, **kwargs):

        context = super(Dialog, self).get_context_data(**kwargs)
        context['header'] = self.request.user.username

        context['today'] = datetime.now()

        if hasattr(self, 'talker_image'): context['talker_image'] = self.talker_image

        return context

    def get_queryset(self, *args, **kwargs):

        qs = super(Dialog, self).get_queryset()

        qs = qs.filter(Target_id=self.dialog)

        qs = qs.annotate(sender_id=Max('Sender__id')).order_by('-id')[:90]

        return qs

    def get(self, *args, **kwargs):

        buddy_id = kwargs.get('to', None)

##        Dialogue.get_for_buddys(self.request.user.id, buddy_id)

        partakers = [buddy_id, self.request.user.id]

        dialogs = Dialogue.objects.annotate(cnt=Count('Partakers')).filter(cnt=len(partakers))

        GetImg = Max if int(buddy_id) > self.request.user.id else Min               # идея была прикольной, сейчас не использую
        Image = Subquery(Profile.objects.filter(dialogs=OuterRef('id')).filter(id=buddy_id).values('Image')[:1])       # .order_by('-id')

        dialogs = dialogs.annotate(talker_image=Image)

        dialog, created = dialogs.filter(Partakers__id=self.request.user.id).get_or_create(Partakers__id=buddy_id)

        if created:
            buddy = Profile.objects.get(id=buddy_id)
##            dialog.Partakers = [buddy, self.request.user]                         ## работал без промежуточной таблицы (11 запросов)
##            dialog.Partakers = [buddy_id, self.request.user.id]                   # то же самое (11 запросов)
##            dialog.Partakers.add(buddy,me)                                        # то же (количество запросов не проверял)

            # так 11 запросов
            Dialogue_Partakers.objects.create(Dialogue=dialog, Profile=self.request.user)
            Dialogue_Partakers.objects.create(Dialogue=dialog, Profile_id=buddy_id)

        self.dialog = dialog.id                                               ## для фильтра dialog.messages в get_queryset
        if (dialog.talker_image): self.talker_image = dialog.talker_image

##        self._update_presence(dialog.id)

        r = super(Dialog, self).get(*args, **kwargs)
        return r

    def post(self, *args, **kwargs):

##        print '******************'
##        print self.request.FILES

        images = self.request.FILES.get('images', None)
        message = images or self.request.POST.get('value', None)

        dialog = None

##      отправка исходящего сообщения:
        if message:

            recipient_id = kwargs.get('to', None)                                  # не None
            dialog_id = None

            if recipient_id:                                                         # получить диалог на основании id пользователя

                partakers = [recipient_id, self.request.user.id]
                dialogs = Dialogue.objects.annotate(cnt=Count('Partakers')).filter(cnt=len(partakers))
                dialogs = dialogs.filter(Partakers__id=recipient_id).filter(Partakers__id=self.request.user.id)
                dialog = list(dialogs).pop() if len(dialogs) else None

            else:                                                                    # получить диалог из адреса

                dialog_id = kwargs.get('dial', None)
                dialog = Dialogue.objects.get(id=dialog_id)

            if type(message) != str:
                from ..utils import FileStorage, STORAGE
                fs = FileStorage((recipient_id or dialog_id) or '', STORAGE.MESSAGES)
                name = fs.image_save(message)
                if name: message = chr(28) + settings.MEDIA_URL + STORAGE.MESSAGES + name
                else:
                    raise Warning('image_save in FileStorage return false. it shouldnt be like this')
##            else:
##                message = ' {}'.format(message)

##                print '----------------------***'
##                print message
                # сохраняем файл в бд


            Message.objects.create(Sender=self.request.user, Content=message, Target=dialog)

##            print 'teeeeeeeeeeeeeeeeext mess getted'

            return HttpResponse(u'_ok_')

##      проверка входящих сообщений:
        else:                                                               #    return JsonResponse({'received' : 'ok'})
            chk = self.request.POST.get('check', None)

            print 'last recieved mess had id: ' + str(chk)

            sender_id = kwargs.get('to', None)

            dialog = None

            if sender_id:

                dialog = Dialogue.get_for_buddys(self.request.user.id, sender_id)

            else:

                dial_id = kwargs.get('dial', None)
                dialog = Dialogue.objects.get(id=dial_id)

            self._update_presence(dialog.id)

            for i in range(10):
##                messages = Message.objects.filter(Sender=sender_id, Target=dialog, id__gt=chk)
##                messages = Message.objects.exclude(Sender=self.request.user).filter(Target=dialog, id__gt=chk)
##                print messages.query
                messages = Message.objects.filter(Target=dialog, id__gt=chk).exclude(Sender=self.request.user)

                if len(messages):

                    print 'find new messages by longpoll: ' + str(len(messages))
##                    print messages
##                    data = serializers.serialize('json', messages, fields=('Content',))
##                    data = json.dumps(list(messages.values('id', 'Content')))
##                    data = {}
##                    for mess in messages:
##                        data[mess.id]=mess.Content


                    data = { mess.id : mess.Content for mess in messages }

##                    self._update_presence(dialog, max(data.keys()))                 # наибольшее ид из полученных сообщений

                    return JsonResponse(data)
                time.sleep(1)

            return HttpResponse('nop')



##from django.shortcuts import render_to_response
##def dialtest(request, dial):
##    qs = Message.objects.filter(Target_id=dial)
##    qs = qs.annotate(sender_id=Max('Sender__id'))     #                                 [0:100] - либо тут, но до 150 мс, иначе 400мс
##    qs = qs.order_by('-id')[:10][::-1]
##    return render_to_response("message_test.html", {'messages':qs, 'user':request.user})



@method_decorator(login_required, name='dispatch')
class MultiDialog(Dialog):

##    def get_queryset(self, *args, **kwargs):
##
##        qs = super(MultiDialog, self).get_queryset()
##

##        qs = qs.annotate(latest=Max('Time')).filter(Time__gt=F('latest')-timedelta(days=1))
##        qs = reversed(qs.order_by('-id')[:10])
##        print qs[0].latest - timedelta(days=1)                                            #почему-то считается неверное время
##        qs = Message.objects.annotate(sender_id=Max('Sender__id')).filter(Target_id=self.dialog)[:100]
##
##        qs = Message.objects.filter(Target_id=self.dialog)
##        qs = qs.annotate(sender_id=Max('Sender__id'))     #                                 [0:100] - либо тут, но до 150 мс, иначе 400мс
##        qs = qs.order_by('-id')[:90]

##
##        return qs


    def get(self, *args, **kwargs):

        dialog_id = kwargs.get('dial', None)

        #dialog = Dialogue.objects.get(id=dialog_id) #                                  SELECT ••• FROM "main_dialogue" WHERE "main_dialogue"."id" = '22'

        self.dialog = dialog_id                                                           ## для фильтра dialog.messages в get_queryset

##        self._update_presence(dialog_id)

##        вызывает не родителя MultiDialog - вызывает непосредствыенно ListView
        return super(Dialog, self).get(*args, **kwargs)



