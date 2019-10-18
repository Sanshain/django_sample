# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import chain
import json


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
from django.http import HttpResponseRedirect  											              # для AJAX
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator



# main
from main.models import Profile, Friends, State
from main.models.messages import Dialogue, Message, Dialogue_Partakers
from main.views.Mixins import CSSMixin
from ..forms import create_note
from ..models.notes import Article
from ..utils.utime import present_time

if settings.DEBUG:
    from datetime import timedelta, datetime
    import time
    import timeit
    import traceback


class note_create(CreateView):
    model = Article
    template_name = '_newnote.html'
    succes_url = '/success/' 									                    # reverse_lazy('contact') или reverse
    form_class = create_note
    succes_urls = '/success/'
##    fields = ['Title','Content']                                                                     # '__all__'

    def post(self, request, *args, **kwargs):
        print '++++++++++++++++++'
        self.form_class.user = self.request.user

        received_json_data=json.loads(self.request.body)
        print received_json_data

        a  = Article(Title=received_json_data['id_Title'], Content=received_json_data['id_Content'], From=self.request.user)
        print a.Content
        a.save()
        #initial=received_json_data,
##        note = create_note(instance=a)
##        received_json_data.update({'id_From':self.request.user.id})
##        note = create_note(initial=received_json_data)
##        if note.is_valid():
##            print note


        base_post = super(note_create, self).post(request, *args, **kwargs)

        return JsonResponse({'title' : a.Title, 'content': a.Content} )

##    не исполняется почему-то:
##    def form_valid(self, form):
##        return super(note_create, self).form_valid(form)