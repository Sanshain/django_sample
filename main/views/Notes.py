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
from ..utils import FileStorage, STORAGE

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

##    fields = ['Title','Content']                                                                     # '__all__'

    def post(self, request, *args, **kwargs):

        self.form_class.user = self.request.user

##        note_texts=json.loads(self.request.body)                                  # если получать только JSON, то работает
        note_texts=json.loads(self.request.POST.get('texts', ''))

        note_images = self.request.FILES.getlist('images', None)

        fs = FileStorage(self.request.user.id, STORAGE.NOTES)

        imgs = []

        for image in note_images:

            name = fs.image_save(image)

            imgs.append(name)

        images = json.dumps(imgs)                                                   # toString()

        a  = Article(
            Title=note_texts['id_Title'],
            Content=note_texts['id_Content'],
            Images=images,
            From=self.request.user
        )
        a.save()


        # то же самое (сохранение) через ModelForm:
##        note_form = create_note(instance=a)
##        note_texts.update({'id_From':self.request.user.id})
##        note_form = create_note(initial=note_texts)
##        if note_form.is_valid():
##            print note_form


        base_post = super(note_create, self).post(request, *args, **kwargs)

        return JsonResponse({
            'title' : a.Title, 'content': a.Content, 'images': imgs
        })

##    не исполняется почему-то:
##    def form_valid(self, form):
##        return super(note_create, self).form_valid(form)


class ArticleView(CSSMixin, DetailView):
    model = Article
    template_name = '{}.haml'.format(model._meta.object_name.lower())

    def get_object(self, queryset=None):

        obj = super(ArticleView, self).get_object()

        #obj = obj.select_related('From')

        return obj


    def get_queryset(self):

        qs = super(ArticleView, self).get_queryset()

        qs = qs.select_related('From')

        return qs