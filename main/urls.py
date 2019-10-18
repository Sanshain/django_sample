# -*- coding: utf-8 -*-
"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:			from main.views.pages.Profile import *
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')					from main.views.Profile import *
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='h
    ome')				from main import views
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include			from django.urls import path
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))		    		path('', views.index, name='home'),
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import admin

from django.views.generic import TemplateView, CreateView

from main.views.pages import ProfileView
from main.views.Messages import Dialogs, Dialog, MultiDialog
from main.views.fragments.Users import read_friends
from .views.Notes import note_create
from main.models import Raiting
from .views.fragments.Dialog import bring_dialog

urlpatterns = [
    url(r'^user/$', ProfileView.Mirror, name='Me'),                                             # я сам
    url(r'^users/(?P<pk>[0-9]+)/',login_required(ProfileView.UserView.as_view()), name = 'user'),         # число в аргументе, страница польз-ля
    url(r'^users/$', ProfileView.UserList.as_view(), name='users'),                                         # список друзей
    url(r'^$', ProfileView.Load, name='Profile_Load'),
	url(r'^about/$', TemplateView.as_view(template_name="about.htm")),
	url(r'^signme/$', ProfileView.Create.as_view()),
	url(r'^signup/$', ProfileView.SignUp.as_view(), name= 'signup'),
    url(r'^signin/$', ProfileView.SignIn.as_view(), name= 'signin'),
    url(r'^signout/$', LogoutView.as_view(next_page='/signin/'), name= 'signout'),                       # LogoutView.as_view(next_page = '/signin/'),
	url(r'^success/$', TemplateView.as_view(template_name="gradulation.html"), name='gradulation'),
    url(r'^edit_self/(?P<pk>[0-9]+)/', ProfileView.UserUpdate.as_view(), name= 'edit_self'),

    url(r'^messages/to_(?P<to>[0-9]+)/', Dialog.as_view(), name= 'dialog'),
    url(r'^messages/$', Dialogs.as_view(), name= 'dialogs'),
    url(r'^dialog/(?P<dial>[0-9]+)/', MultiDialog.as_view(), name= 'multidialog'),
##    url(r'^dialog/(?P<dial>[0-9]+)/', dialtest, name= 'multidialog'),


    #url(r'^raiting/$', CreateView.as_view(model=Raiting, template_name='main/create_raiting.html'))
    url(r'^raiting/$', ProfileView.CreateRate.as_view()),
    url(r'^note_create/$', note_create.as_view(), name='note_create'),

    # AJAX:
    url(r'^to_friend/$', ProfileView.ToFriend, name='to_friend'),
    url(r'^get_friends/$', read_friends, name='get_friends'),
    url(r'^get_dialog/$', bring_dialog, name='get_dialog')
]

if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)             #{'document_root': settings.MEDIA_ROOT,}
##
##if settings.DEBUG:
##    import debug_toolbar
##    urlpatterns = [
##        url(r'^__debug__/', include(debug_toolbar.urls)),
##    ] + urlpatterns

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)                             # можно и так

