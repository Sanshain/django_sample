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
from main.forms import common
from main.forms import user
from main.forms.note import RatingForm, create_note
from main.views.Mixins import CSSMixin

if settings.DEBUG:
    from datetime import timedelta, datetime
    import time
    import timeit



@login_required
def to_friend(request):

    if request.method == "POST":
        user_id = request.POST.get("id",'')
        user = Profile.objects.get(id=user_id)

        #надо найти оба вхождения (by и friend) и (friend и by)
        friends = Friends.objects.filter(Q(by=request.user, friend=user) | Q(friend=user,by=request.user))
        if friends.exists():
            friends.delete()
        else:
            Friends.objects.create(by=request.user, friend=user)

        return HttpResponse('us_' + user_id )
    else:
	   return HttpResponseRedirect(reverse('users'))


##        friends = Friends(by=request.user, friend=user)
##        friends.save()



def read_friends(request):
    if request.method == "POST":
        user = request.POST.get("id", None)
        if user == '0':

#           минус в том, что все поля:
##            data = Profile.objects.get(id=request.user.id).pals.only('id','username')
##            data = serializers.serialize("json", data)                      # https://stackoverflow.com/questions/26373992/use-jsonresponse-to-serialize-a-queryset-in-django-1-7

##          несколько неудобно:
##            data = Profile.objects.get(id=request.user.id).pals.all()
##            data = [{'id':d.id, 'username' : d.username} for d in data]


            image = u'life__Image'
            friends = list(Profile.objects.get(id=request.user.id).pals.values('id','username', image))
##            return JsonResponse(friends, safe=False)

            img = None
            people = buffer(b'')

            print '______profiling for read_friends()_______'
            a = timeit.default_timer()

            for friend in friends:
                img = friend.pop(image)

                t = time.time()


                buf = json.dumps(friend) + chr(30)                                      # str(len(buf)).zfill(3)
                print 'source len of convert img is %s bytes'%len(img)

                #Image.fromarray(img)
                #Image.frombytes(img)
                #Image.fromstring
                #Image.frombuffer
                img = buffer(base64.b64encode(img))                                     # base64
                people += buffer(buf + str(len(img)).rjust(5, b'0')) + img      # http://qaru.site/questions/49614/what-is-python-buffer-type-for

            print 'preparation convert img to base64 holds %s ms'%(timeit.default_timer()- a)


##                one_man = ''
##                for attr in friend:
##                    one_man += str(friend[attr]) +  chr(30)
##                buf = buffer(chr(31) + one_man + chr(29) + str(len(img)).rjust(5, b'0'))

##            return HttpResponse(ByteIO(people), content_type='text/plain')            # не проверял
##            return HttpResponse(people, content_type='text/plain')
##            response = HttpResponse(people, content_type='image/jpeg')
##            response = HttpResponse(people, content_type='application/zip')

            print 'agregated by async friends reading data:uri hold %s bts'%len(people[:])
            print '______end profiling for read_friends()_______'

            response = HttpResponse(people, content_type='application/x-binary')

            return response

        else:

            data = Profile.objects.get(id=user).pals.values()
            return JsonResponse(data, safe=False)
    else:

        return JsonResponse({})



