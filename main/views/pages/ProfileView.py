# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# для процедурного стиля:

import os
from os.path import dirname as up;
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

from main.views.Mixins import CSSMixin, ReactMixin

#common_init.py:
from django.utils.translation import ugettext_lazy as _

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

    def _set_css(self, context):

        profile = self.object                                                         #get_object() - делает один лишний запрос
        if not profile.Image:
            context['links'].append(context['links'][0][:-4] + u'/default_avatar.css')


    def _get_model_fields(self, args):

        cuser, user_id = args

        user_fields=('Age','City','Sex','Image')
        user_dict = model_to_dict(cuser, user_fields)

        user_dict['Image'] = cuser.Image.url
        #user_dict['username'] = '{} {}'.format(cuser.first_name, cuser.last_name)
        user_dict['Age'] = user_dict['Age'].strftime("%d.%m.%Y") if user_dict['Age'] else ''

##            from os.path import dirname as up; print up(up(up(__file__)))
##            print os.path.abspath(os.path.join(__file__ ,"../../.."))
        #https://askdev.ru/q/python-poluchit-katalog-na-dva-urovnya-vyshe-73156/


##            pathname = up(up(up(__file__))) + settings.STATIC_URL                   #  settings.BASE_DIR
##            js_func = ''
##            with open(pathname + 'js/_get_dialog.js') as file_handler:
##                js_func = file_handler.read()

        if cuser == self.request.user:
            user_dict['action'] = {
                'innerHTML': ('Измениться'),
                'name' : '',
                'formAction' : reverse('edit_self', args=[user_id]),
                'onclick' : 'do_action(this, event)'
            }
        else:
            user_dict['action'] = {
                'innerHTML':'Отправить сообщение',
                'name' : reverse('get_dialog').strip('/'),                                  # то, куда будет отправлен пост-запрос
                'formAction' : reverse('dialog', args=[user_id]),                           # адрес, по которому доступен результат

                'onclick' : 'fragment_refresh(event)',
				'data-_refresh' : 'content',
				'data-_require' : 'aside',
            }
        #user_dict.update({'note_create' : {'style':'display:none'} })

        return user_dict



    def get_context_data(self, *args, **kwargs):                                    # расширение контекста

        context = super(UserView, self).get_context_data(*args, **kwargs)

        context['header'] = "Профиль"
        context['articles'] = Article.objects.filter(From = self.object)[::-1]  #
        context['create_articles'] = create_note
        #context['to_dialog'] = reverse('get_dialog').strip('/')
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
        #тут приходит только user_id/ теперь будет приходить еще и

        print self.request.content_type
        print (self.request.body)

        q = json.loads(self.request.body)

        print q

        aim = q.pop()
        if len(aim) > 10: return JsonResponse({'Exception':'Too large object'})

        blocks = q.pop()
        print q
        user_id = q.pop()[0]
        print user_id

##        user_id= self.request.body.split('&')[-1:][0]
##        print user_id




        cuser = Profile.objects.get(id=user_id)                                      # .values('id','username')
        articles = Article.objects.filter(From=cuser)                               ## articles = cuser.inote.select_related('article').filter(article__isnull=False))


        def _render_fragment(args):

            #template_name, context, surround = args

            request = args[1].pop('request', None)                                     # извлекаем request из 2-го аргумента

            templ = render_to_string(
                'fragments/%s.html'%args[0],
                context=args[1],
                request=request
            ).strip()

            if len(args) == 3:
                surround = args[2]                                                     # кортеж из класса и id элемента

                if len(surround) == 2:
                    return "<div class='{}' id='{}'>{}</div>".format(*(surround + (templ,)))
                else:
                    return "<div class='{}'>{}</div>".format(*(surround + (templ,)))
            else:
                return templ

        #templates - dict as template_name:(context, surround)
        def _render_root_fragment(templates):

            blocks = []
            for tmpl in templates:
                blocks.append(_render_fragment(tmpl))

            return '{}{}{}{}{}{}'.format(
                "<div id='main'>",blocks[0],'</div>',
                "<div id='section'>", blocks[1] ,"</div>")




        # окружение для вариативных шаблонов:
        user_env = ["_user_profile", {
            'self' :  cuser == self.request.user,
            'user' : self.request.user,
            'profile':cuser }, ('left_block',)]                                   # ,'user_block'

        article_env = ["articles_main", {
            'articles':articles,
            'request' :self.request }, (
                'centre_block', 'articles_block')]

        patterns = {
            #при любом раскладе:
            'header' : (lambda x: '{} {}'.format(x.first_name, x.last_name), cuser),


            #вариативные шаблоны:
            'content': (_render_root_fragment, [user_env, article_env]),

            #два одинаковых
            '<article' : (_render_fragment, article_env),
            'section' : (_render_fragment, article_env),                           # was used in a template, but the context did not provide the value. This is usually caused by not using RequestContext

            'main' : (_render_fragment, user_env),

            # минорные вариат шаблоны:
            'inside' : (_render_fragment, ['newnote_modalform', {
                'profile':cuser,
                'user' : self.request.user
            }]),

            # при самом мизерном (точечном) изменении:
            '*main' : (self._get_model_fields, [cuser, user_id]),

            # вне контекста (опциональные):

        }
        #patterns.prepare = lambda x: x[0](x[1])


        user_dict = {}
        for key in aim:

            resp_raw = patterns.get(key, (lambda x: "", None))
            respond = resp_raw[0](resp_raw[1])                                     # patterns.prepare(resp_raw)
            if type(respond) is dict:
                user_dict.update(respond)
            else: user_dict[key] = respond

        user_dict['dynamic_link'] = settings.STATIC_URL + 'style/user.css'

        print '99999999999999999999999'
        print user_dict['action'] if 'action' in user_dict else '////////'

        ret = json.dumps(user_dict)                                                 # работает, если убрать связь 1:8
        return JsonResponse(ret, safe=False)



##
##
##
##
##
##        preferer = self.request.META.get('HTTP_REFERER','')
##        print preferer
##
##        user_dict = {}
##        if 'user' in preferer:
##
##            user_dict = self._get_model_fields(cuser)
##
##            articles_block = render_to_string(
##                "fragments/articles_main.html",
##                context={
##                    'articles':articles
##                }
##            )
##            user_dict['articles_block'] = articles_block
##
##        else:
##            user_block = render_to_string(
##                "fragments/_user_profile.html",
##                context={
##                    'profile':cuser
##                }
##            )
##            articles_block = render_to_string(
##                "fragments/articles_main.html",
##                context={
##                    'articles':articles
##                }
##            )
##            user_dict['content'] = '{}{}{}{}{}{}'.format(
##                "<div id='main'><div class='left_unit' id='user_block'>",
##                    user_block.strip(),
##                '</div></div>',
##                "<div id='section'><div class='articles' id='articles_block'>",
##                    articles_block,
##                "</div></div>")
##            user_dict['dynamic_link'] = settings.STATIC_URL + 'style/user.css'
##
##        ret = json.dumps(user_dict)                                                 # работает, если убрать связь 1:8
##
####        user_fields=('username','Age','City','Sex','Image')
####        ret = serializers.serialize('json', [user,], fields=user_fields)
####        print ret
##
##
##        return JsonResponse(ret, safe=False)

@method_decorator(login_required, name='dispatch')
class UserUpdate(UpdateView):
    model = Profile
    context_object_name = 'profile'
    login_url = '/signin/'                                                          # только для Mixin, reverse('signin') - не работает
    success_url = '/users/'                                                         # переопределен get_success_url


    #def get(self)


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

class UserList(LoginRequiredMixin, ReactMixin, ListView):
    model = Profile
    # template_name = "home.html" 							                       	# по умолчанию main/profile_list.html
    template_name = 'main/profile_list_2.haml'
    context_object_name = 'Users'							                    	# object_list by default
    login_url = '/signin/'

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        #надо получить состояние о дружбе о всеми:
        friends = Friends.Find((Q(by=self.request.user) | Q(friend=self.request.user)), approve=State.Yes)

        context['header'] = self.request.user.username
        return context

    def get_queryset(self, **kwargs):


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

    def post(self, request, *args, **kwargs):
        q = json.loads(request.body)


        requested_blocks = q.pop()
        if len(requested_blocks) > 10: return JsonResponse({'Exception':'Too large objects'})
        requared_blocks = q.pop()

        filter_param = q.pop()






        # block_name ='content' должен задаваться на уровне LightReact как поле
        block_name ='content'
        css_ajax = True

        def _get_samples(
                _block_name=None, _filter_param=None, _template=None, css__cls_id=None):
            """
            _block_name - имя блока (id) на странице. По дефолту = block_name класса
            _filter_param - должен быть словарем
            _template - имя шаблона, по дефолту равно _(_)model_name(s)
            _css__cls_id - id и class тега для заворачивания. По дефолту не заворачивает
            """

            filter_param = _filter_param or {}

            _block_name = _block_name or block_name

            if not _block_name:
                raise Exception('block_name is nit defined')
                return {}

            s = 's' if ListView in self.__class__.__mro__ else ''

            # можно так же вычислять на основе template_name.split('/')[-1].split('.')[0]
            _template_name = _template or '_%s%s%s'%('_' if s else '', self.model.__name__.lower(), s)
            _prime_key = self.context_object_name or ('object_list' if s else 'object')
            _prime_value = self.get_queryset(**filter_param) if s else self.get_object()


            prime_env = [
                _template_name, {_prime_key : _prime_value,  'request' :self.request }]

            if css__cls_id: prime_env.append(css__cls_id)

            sample_dict = {
                _block_name : (self._render_fragment, prime_env)}

            return sample_dict



        def fill_response_for(_requested_blocks, _by_samples = None):
            """

            _requested_blocks - требуемые блоки для заполнения
            _by_samples - образцы. Если они не заданы, то будут вычислены дефолтные на основе _get_samples() и block_name

            """

            _by_samples = _by_samples or _get_samples()

            _field_dict = {k : fa[0](fa[1]) for k, fa in _by_samples.iteritems() if k in _requested_blocks}

            if CSSMixin in self.__class__.__mro__:
                _field_dict.update(self.get_default_style('post'))
            elif css_ajax:
                _field_dict['dynamic_link'] = self.template_name.split('/')[-1].split('.')[0] + '.css'

            return _field_dict


        field_dict = fill_response_for(requested_blocks)

        j = json.dumps(field_dict)

        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>'
        print field_dict.keys()
        return JsonResponse(j, safe=False)


##        _template_name = '__profiles'
##
##        _query_set = self.get_queryset(filter_param)
##
##        sample_dict = {
##            'content' : (self._render_fragment, [_template_name, {
##                                            'Users': self.get_object(),
##                                            'request' :self.request
##                                        },('centre_block', 'article')])                                         # - id, class
##
##        }








class Create(CreateView):
    form_class = user.CreatePerson
    template_name = 'registration/welcome.html'
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
    template_name = 'registration/signup.html'
    succes_url = '/success/'

    def get_context_data(self, **kwargs):

        print '+++++++++++++++++++++'

        context = super(SignUp, self).get_context_data(**kwargs)

        print '---------------------'

        context['form'].request = self.request

        print '===================='

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



