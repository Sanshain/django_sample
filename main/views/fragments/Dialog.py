# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import base64

# для процедурного стиля:

from django.core import serializers
from django.shortcuts import render						# для страниц, или ниже:
from django.template.response import TemplateResponse 	# для страниц 		https://stackoverflow.com/questions/38838601/django-templateresponse-vs-render
from django.http import HttpResponse, JsonResponse, FileResponse

# для cbv-стиля:
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView               # для страниц
from django.shortcuts import redirect														              # для переадресации псле валидации
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect    											              # для AJAX
from django.urls import reverse
from django.utils.decorators import method_decorator


# main
from main.models import Profile, Raiting, Article, Friends, State
from ...models.messages import Dialogue, Message
from main.forms import common
from main.forms import user
from main.forms.note import RatingForm, create_note
from main.views.Mixins import CSSMixin

if settings.DEBUG:
    from datetime import timedelta, datetime
    import time
    import timeit


from django.template.loader import render_to_string
from django.db.models import Min, Max

from ..Mixins import LightReact


@login_required
def bring_dialog(request):
    '''
    Получение диалога
    '''
    if request.method == "POST":
        user_id = request.POST.get("id",'')

        print '----------------------'
        print user_id

        dialog = Dialogue.get_private_Dialog(user_id, request.user.id)
        dialog_id = dialog.id



        messages = Message.objects.filter(Target_id=dialog_id)

        choose_sender = Max if int(request.user.id) < user_id else Min

        messages = messages.annotate(sender_id=choose_sender('Sender__id'))
        messages = messages.order_by('-id')[:90]

        messages_block = ["messages_list", {
            'buddy_id' : user_id,
            'user' : request.user,
            'messages' : messages,
            'talker_image' : settings.MEDIA_URL + dialog.talker_image
        }]

        context = {
            'content': LightReact.render_root_fragment((messages_block, "")),
            'dynamic_link': settings.STATIC_URL + 'message_list.css',
            'dynamic_c_list': settings.STATIC_URL + 'js/message_list.js',
        }

        data = json.dumps(context)

        return HttpResponse(data, content_type="application/json")
    else:
	   return HttpResponseRedirect(reverse('users'))

