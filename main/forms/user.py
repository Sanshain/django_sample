# -*- coding: utf-8 -*-


from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import NON_FIELD_ERRORS

# модели:
from main.models import Profile


# для кастомного Field:
from django.forms import BoundField, Field, ImageField
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

# для вывода {{form}} в шаблон
from django.middleware.csrf import get_token

# для кастомной формы форм авторизации:
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError

from .common import HTMLForm, ViewImageField, CustomImageField, HTMLMixin, HTMLabelForm


class CreatePerson(HTMLForm):

    """
    Кастомная форма, как в user2, только наследованная от html-формы
    """
    #required_css_class = 'required_fields'
    error_css_class = 'error_class' 	#работает, но не востребовано

    class Meta(object):

        model = Profile
        fields =  ('username', 'password', 'first_name', 'last_name', 'email', 'City', 'Sex', 'Age', 'Image') 		# exclude
		#exclude = ('username',)
        labels = {
            'username': 'Введите желаемый логин',
            'password': 'Пароль',
            'first_name': 'Имя',
            'last_name': 'Фамилия либо Отчество',
            'email': 'Почта',
			'Image':'Изображение',
        }
        help_texts = {
            'username': (''),
        }
        widgets = {
		    'password': forms.PasswordInput(attrs={'placeholder': u'Пароль'}),
            'email': forms.EmailInput(attrs={'placeholder':'mail@example.ru'}),
    		'Image': forms.FileInput(
    			attrs={
    				'accept':"image/jpeg,image/png",
    				'style':'visibility:hidden',
    				'onchange': 'file_upload(this, event)'}),#'style':  display:none
		}

        """
		'Image': forms.FileInput(
			attrs={
				'accept':"image/jpeg,image/png",
				'style':'visibility:hidden',
				'onchange': 'file_upload(this, event)'}),#'style':  display:none
        """

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.", 	#если нужны будут два уникальных поля
            },
            'username': {
                'unique': u"Пользователь с таким именем уже существует",
            },
        }

    def additional_init(self, *args, **kwargs):
        print 'ddd_'
        if 'email' in self.fields:
            self.fields['email'].validators=[EmailValidator(message="Некорректный адрес электронной почты")]

    def __init__(self, *args, **kwargs):
        super(CreatePerson, self).__init__(*args, **kwargs)
        self.submit = u'Присоединиться'
        self.css_class = ''
        self.enctype = self.Enctype(self.Enctype.Multipart)

        self.fields['Image'] = CustomImageField(self.fields['Image'])
        self.additional_init(*args, **kwargs)

    # не происходит!
    def post(self, request, *args, **kwargs):
        print '============'
        return super(CreatePerson, self).post(*args, **kwargs)



class SignUpForm(UserCreationForm, HTMLabelForm):
    """
    Венец труда. Переопределены основные ошибки. Форма авторизации пользователя
    """
    class Meta:

        model = Profile
        fields = ("username", "email", "password1", "password2")		#
        labels = {
            'username': 'Имя',
        }
        help_texts = {
            'email': 'Введите правильный e-mail',
            'password1': ('Не совпадает пароль'),
			'password2': ('Не совпадает пароль'),
        }


    email = forms.EmailField(required=True, label='Почта')

    error_messages = {
		'password_mismatch': "Два пароля не совпадают",
	}

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Profile.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Вы уже зарегистрированы на этот адрес")
        return email

    def __init__(self, *args, **kwargs):


        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повторите пароль'

        self.fields['email'].validators=[EmailValidator(message="Некорректный адрес электронной почты")]

        HTMLabelForm.tag = 'p' #почему не работает self
        self.submit = u'Присоединиться'

    def save(self, commit=True):
		#надо по идее убрать из Мета лишние поля. В  UserCreationForm они не добавляются почему-то
        user = super(SignUpForm, self).save(commit=False)
		#user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user



class SignForm(HTMLMixin, AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):

        super(SignForm, self).__init__(*args, **kwargs)
        self.css_class = self.cls.lower()
        self.tag = 'p class="signin"'
        self.submit = u'Войти'


