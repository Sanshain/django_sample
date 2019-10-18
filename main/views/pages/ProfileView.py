# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# для процедурного стиля:

import os
import io
import json
from PIL import Image

from django.conf import settings
from django.core import serializers


from django.shortcuts import render						# для страниц, или ниже:
from django.template.response import TemplateResponse 	# для страниц 		https://stackoverflow.com/questions/38838601/django-templateresponse-vs-render
from django.http import HttpResponse, JsonResponse

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
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator


# main
from main.models import Profile, Life, Raiting, Article, Friends, State
from main.forms import common
from main.forms import user
from main.forms.note import RatingForm, create_note

from django.forms.models import model_to_dict

from main.views.Mixins import CSSMixin

if settings.DEBUG:
    from datetime import timedelta, datetime
    import time
    import timeit

# Create your views here. В процедурном стиле:
@login_required
def Load(request):
    # return HttpResponse("Hello World!")
	return render(request, "load.html")

##        print user.from_friend
##        username = request.POST.get("login",'')
##        Profile.objects.get_by_natural_key(username)

@login_required
def ToFriend(request):

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



"""
на себя переадресация, чтобы избежать аргументов в get_absolute_url модели:
"""
@login_required
def Mirror(request):
	return HttpResponseRedirect(reverse('user', kwargs={'pk': request.user.id}))



# В Класс-V-стиле TemplateView
#@method_decorator(login_required, name='dispatch')
class UserView(CSSMixin, DetailView):
    model = Profile
    template_name = "user.html"
    context_object_name = 'profile'                                                 # по умолчанию object
    #login_url = '/signin/'                                                         # для LoginRequiredMixin

    def set_css(self, context):

        profile = self.object                                                         #get_object() - делает один лишний запрос
        if not profile.Image:
            context['links'].append(context['links'][0][:-4] + u'/default_avatar.css')

    def get_context_data(self, *args, **kwargs):                                    # расширение контекста

        context = super(UserView, self).get_context_data(*args, **kwargs)

        context['header'] = "Профиль"
        context['articles'] = Article.objects.filter(From = self.object)[::-1]  #
        context['create_articles'] = create_note
        if self.request.user.id == kwargs['object'].id:
            context['self'] = True

        return context

    """
    def render_to_response(self, context, **response_kwargs):                       # для замера скорости рендеринга

        #start = time.clock()
        start = timeit.default_timer()

        hr = super(Detail, self).render_to_response(context, **response_kwargs)

        #delta = time.clock() - start
        delta = timeit.default_timer() - start

        print delta
        print datetime.fromtimestamp(delta)
        #print timedelta(seconds=round(delta))

        return hr
    """

    def post(self, *args, **kwargs):
        user_id= self.request.body.split('&')[-1:][0]
        cuser = Profile.objects.get(id=user_id)                                     #(id=user_id).first()   # .values('id','username')

        articles = Article.objects.filter(From=cuser)
##        articles = cuser.inote.all()
##        print articles

        user_fields=('Age','City','Sex','Image')
        user_dict = model_to_dict(cuser, user_fields)
        user_dict['Image']=cuser.Image.url
        user_dict['username'] = cuser.first_name + ' ' +  cuser.last_name
        if user_dict['Age']:
            user_dict['Age'] = user_dict['Age'].strftime("%d.%m.%Y")

        articles_block = render_to_string("fragments/articles_main.html",context={'articles':articles})
        user_dict['articles_block'] = articles_block

        ret = json.dumps(user_dict)                                                 # работает, если убрать связь 1:8

##        user_fields=('username','Age','City','Sex','Image')
##        ret = serializers.serialize('json', [user,], fields=user_fields)
##        print ret


        return JsonResponse(ret, safe=False)

@method_decorator(login_required, name='dispatch')
class UserUpdate(UpdateView):
    model = Profile
    context_object_name = 'profile'
    login_url = '/signin/'                                                          # только для Mixin, reverse('signin') - не работает
    success_url = '/users/'                                                         # переопределен get_success_url

    def additional_init(self, *args, **kwargs ):
        self.submit = 'Сохранить'

        for field_key in self.fields: self.fields[field_key].required = False


    form_class = type(str('Edit_Profile'), (user.CreatePerson,), {
        'Meta':type(str('Meta'), (user.CreatePerson.Meta,) ,{
            'fields' : ('first_name', 'last_name', 'City', 'Sex', 'Age', 'Image'),
            'labels' : {
                'first_name': 'Имя',
                'last_name': 'Фамилия либо Отчество',
                'City': 'Город',
                'Sex' : 'Пол',
                'Age' : 'Дата рождения',
    			'Image':'Изображение',
            },
        }),
        'additional_init' : additional_init                                         # lambda self, *args, **kwargs: None
    })

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context['form'].request = self.request
        context['links'] = [settings.STATIC_URL + 'form.css']
        return context


    def get_success_url(self):
        return reverse('user', args=[self.object.id])


    def form_valid(self, form, **kwargs):
        if not form.is_valid():
            return super(UserUpdate, self).form_valid(form, **kwargs)

        result = super(UserUpdate, self).form_valid(form, **kwargs)

##        print form.cleaned_data['Image'].file
##        print self.request.FILES['Image']

##        print form.instance.Image.path

##        with open(form.cleaned_data['Image'].path, "rb") as image:
##            pass
##        print form.cleaned_data['Image']




        print '-------------------;'


##        size = (50, 50)

        image = Image.open(form.instance.Image.path)                                # form.instance.Image.path дбыть после сохранения!

##        print type(image)
##        print form.instance.Image.path
##        print dir(image)
##        image.save("D:\\lenna.jpeg")
##        image.show()
##        binary = image.tobytes()
##        print len(binary)

##        image.thumbnail(size)                                                     # то же что resize, но с сохранением пропорций
        image = image.resize((40, 40), Image.HAMMING)                            # https://ru.stackoverflow.com/questions/909680/pillow-image-antialias-vs-image-hamming
        tempfile_io = io.BytesIO()
        image.save(tempfile_io, 'JPEG')
        v = tempfile_io.getvalue()
##        print type(tempfile_io)
##        print dir(tempfile_io)
##        print len(v)                                                              # настоящая картинка
##        print type(binary)
##        print type(life[0].Image)

        life = Life.objects.get_or_create(Leaser=form.instance)
        self.request.user.life.Image = v                                            # binary
        self.request.user.life.save()


##        uploaded_file = form.files['Image'].file                                    # I assume a `InMemoryUploadedFile` instance
##        data = uploaded_file.file.read()

##        main_app = settings.AUTH_USER_MODEL.split('.')[0]
##        print os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, str(form.cleaned_data['Image'])).replace('\\','/')

        return result


# В Класс-V-стиле

class UserList(LoginRequiredMixin, ListView):
    model = Profile
    # template_name = "home.html" 							                       	# по умолчанию main/profile_list.html
    context_object_name = 'Users'							                    	# object_list by default
    login_url = '/signin/'

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        #надо получить состояние о дружбе о всеми:
        friends = Friends.Find((Q(by=self.request.user) | Q(friend=self.request.user)), approve=State.Yes)

        context['header'] = self.request.user.username
        return context

    def get_queryset(self):

        qs = super(UserList, self).get_queryset()



        #friends = Friends.objects.filter(by=self.request.user)                                     # Find
        #friends = Profile.pals.through.objects.filter(approve=State.No)                            # self.request.user
        #recipients = friends.values_list('friend_id', flat=True)
        #recipients = Profile.Find(id__in=Profile.pals.through.objects.filter(approve=State.No).values_list('friend_id', flat=True))
        #recipients = Profile.objects.filter(to_friend__approve=State.No)                           # self.request.user

        #friends = qs.filter(from_friend__friend = me)                                             # взаимно друзья
        #recipients = qs.filter(to_friend__approve=State.No)                                       # все получатели, не одоб





        me = self.request.user

        recipients = qs.filter(to_friend__by = me, to_friend__approve=State.No)                    # получатели от меня, не одоб
        senders = qs.filter(from_friend__friend = me)                                              # те, кто отправил мне

        for pal in qs:
            if pal == self.request.user:
                pal.Me = True
            elif pal in recipients and pal in senders:
                pal.Friend = True
            elif pal in recipients:                                                                 # if recipient.id in recipients:
                pal.Recipient = True                                                                # отправлены, но не приняты
            elif pal in senders:
                pal.Sender = True

        return qs

class Create(CreateView):
    form_class = user.CreatePerson
    template_name = 'welcome.html'
    succes_url = '/success/' 									# reverse_lazy('contact') или reverse

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        context['form'].request = self.request
        return context

    def form_valid(self, form):
        Profile.objects.create(**form.cleaned_data)
        #suc = self.get_success_url()
		#contact_name = self.form.cleaned_data['contact_name']
        return redirect(self.succes_url)


class CreateRate(CreateView):
    model = Raiting
    form_class = RatingForm
    template_name='main/create_raiting.html'
    #fields = ['Value', 'Target']



class SignUp(CreateView):
    form_class = user.SignUpForm
    template_name = 'welcome.html'
    succes_url = '/success/'

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        context['form'].request = self.request
        return context

    def form_valid(self, form):
        # 'здесь нужно либо подравнять form.cleaned_data'
        # 'либо сохранить из формы'
        print '----------------------------form_valid---------'

		#если UserCreationForm:
        form.save()

		#Если это обычная форма CreatePerson, то прокатит это:
        #Profile.objects.create(**form.cleaned_data)#как теперь оказалось, это не верно:

		#тк мы создаем пользователя, а значит надо использовать auth-модуль:

        #suc = self.get_success_url()
        #contact_name = self.form.cleaned_data['contact_name']
        return redirect(self.succes_url)


class SignIn(LoginView):
    form_class = user.SignForm
    #template_name = login.html по дефолту

    def get_context_data(self, **kwargs):
        context = super(SignIn, self).get_context_data(**kwargs)
        context['form'].request = self.request                                          # для csrf-валидации формы
        context['header'] = 'Вход'
        return context

    def get_success_url(self):
        if self.request.method == 'POST':
            name = self.request.POST.get('username',None)
            if name:
                u = Profile.objects.get_by_natural_key(name)
                return reverse('user', args=[u.id])

        url = reverse('users')
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)



