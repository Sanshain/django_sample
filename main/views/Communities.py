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
from main.views.Mixins import CSSMixin as CssMixin, ReactMixin
from ..forms import create_note
from ..models.notes import Article
from ..utils.utime import present_time

from ..models.communitie import Community
from ..views.Mixins import CSSMixin as CssMixin

if settings.DEBUG:
    from datetime import timedelta, datetime
    import time
    import timeit
    import traceback



from django import forms
class communityValidator(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['title', 'definition']                                        # , 'logo'



class Communie_List(CssMixin, ReactMixin, ListView):
    model = Community
    template_name = 'pages/communities.html'

    def get_queryset(self):

        qs = super(Communie_List, self).get_queryset().order_by('-id')

        return qs

    def post(self, *args, **kwargs):

        q = json.loads(self.request.body)

        aim = q.pop()
        req_blocks = q.pop()
#        object_id = q.pop()[0]

        if len(aim) > 10: return JsonResponse({'Exception':'Too large object'})

        _model = 'communities'                                                       #self.model.__name__.lower()



        sample_dict = {
            'content' : (self._render_fragment, ['_' + _model, {
                'object_list': self.get_queryset(),
                'request' : self.request
            }]),
        }

        field_dict = {
            'dynamic_c_in_head' : settings.STATIC_URL + 'js/_' + _model + '.js',           #self._render_fragment(['_' + _model + '_script.js', {}]),
            'dynamic_link' : settings.STATIC_URL + 'style/' + _model + '.css',
            'dynamic_style' : self._render_fragment(['_' + _model + '_style.css', {}]),
            'content' : self._render_root_fragment([sample_dict['content'][0](sample_dict['content'][1]),''])
        }

        print field_dict['dynamic_c_in_head']

        return JsonResponse(field_dict, safe=False)                                      # HttpResponse('not index of Comminie is ...')


class Communie(CssMixin, DetailView):
    model = Community
    template_name = 'pages/communitie.haml'



    def post(self, *args, **kwargs):

        community_form = communityValidator(self.request.POST)

        print self.request.POST

        if community_form.is_valid():

            community = community_form.save(commit=False)                                      # commit=False
            community.Author= self.request.user
            community.save()

            return HttpResponse(community.id)

        else: print community_form.errors

        return HttpResponse('new1 index of Comminie is ...')

