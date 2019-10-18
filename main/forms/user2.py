# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import NON_FIELD_ERRORS

from main.models import Profile


# для кастомного Field:
from django.forms import BoundField, Field, ImageField
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe




class ImageUpBoundField(BoundField):
    """
    \brief Кастомное отображение поля формы для картинки, скрывающее кнопку и перензначающее
    html-код label: назначает кастомный css-класс для label, по дефолту upload_image

    \Примечание: BoundField отвечает за отображение поля в шаблоне
    """
    def __init__(self, form, field, name, css_cls = 'upload_image'):
        self.css_class = 'class=' + css_cls
        super(ImageUpBoundField, self).__init__(form, field, name)

    def label_tag(self, contents=None, attrs=None, label_suffix=None):

        contents = contents or self.label
        if label_suffix is None:
            label_suffix = (self.field.label_suffix if self.field.label_suffix is not None
                            else self.form.label_suffix)

        if label_suffix and contents and contents[-1] not in _(':?.!'):
            contents = format_html(u'{}{}', contents, label_suffix)
        widget = self.field.widget
        id_ = widget.attrs.get('id') or self.auto_id
        if id_:
            id_for_label = widget.id_for_label(id_)
            if id_for_label:
                attrs = dict(attrs or {}, **{'for': id_for_label})
            if self.field.required and hasattr(self.form, 'required_css_class'):
                attrs = attrs or {}
                if 'class' in attrs:
                    attrs['class'] += ' ' + self.form.required_css_class
                else:
                    attrs['class'] = self.form.required_css_class
            attrs = flatatt(attrs) if attrs else ''
            contents = format_html(u'<label {} {}>{}</label>', self.css_class, attrs, contents)
        else:
            contents = conditional_escape(contents)
        return mark_safe(contents)

class CustomImageField(ImageField):
    """
    Кастомное поле для замены ImageField:

        Подменяет UpBoundField внутри get_bound_field и берет в к-ре настройки с эталонной ImageField
    """

    def get_bound_field(self, form, field_name):
        return ImageUpBoundField(form, self, field_name)

    def __init__(self, required=True, widget=None, label=None, initial=None,
                 help_text='', error_messages=None, show_hidden_initial=False,
                 validators=(), localize=False, disabled=False, label_suffix=None, parent = None):

        if parent:                                                                         # parent имеет тип ImageField
            if isinstance(parent, ImageField):
                label = parent.label
            else:
                raise Exception("type of var `parent` d'not match for ImageField")

        super(ImageUpBoundField, self).__init__(
        		required, widget, label, initial, help_text,
        		error_messages, show_hidden_initial, validators,
        		localize, disabled, label_suffix)


class CreatePerson(forms.ModelForm):

    """
    \brief Созданная вручную CreatePerson-форма.

    \Комментарии: создана для тренировки

    \Недоработки:
        1. в ней нет проверки на совпадение паролей (только одна форма для пароля)
        2. Пароль сохраняеся в виде текста.
        А как мы знаем пароль должн сохранятьсЯ в виде кэша (пользователь должен создаваться через аутентификацию)
    """

    #required_css_class = 'required_fields'
    error_css_class = 'error_class' 														#работает, но не востребовано

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
			'Image':'Ваше изображение',
        }
        help_texts = {
            'username': (''),
        }
        widgets = {
		    'password': forms.PasswordInput(attrs={'placeholder': u'Пароль'}),
            'email': forms.EmailInput(attrs={'placeholder':'mail@example.ru'}),
			#'Image': forms.FileInput(attrs={'accept':"image/jpeg,image/png"}),#'style':'visibility:hidden'  'style':'display:none'
		}
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.", 	#если нужны будут два уникальных поля
            },
            'username': {
                'unique': u"Пользователь с таким именем уже существует",
            },
        }

    def __init__(self, *args, **kwargs):
        super(CreatePerson, self).__init__(*args, **kwargs)

        self.fields['email'].validators=[EmailValidator(message="Некорректный адрес электронной почты")]
        self.fields['Image'] = CustomImageField(label=self.fields['Image'].label)
        #self.fields['username'].validators=[EmailValidator(message="Пользователь с таким именем уже существует")]
        #self['username'].label = 'asasasasasasasasa'    									#тоже работает, но меняет лишь содержимое тега
        """
        for field in self.fields.itervalues():
            field.widget.attrs.update({'class':'user'}) 									#назначаем класс для каждого widgets
        """

	#def form_valid(self, form):
	#def get_initial(self):
	#def get_default_attrs(self):












"""Какая-то экспериментальная TextInput. Она должна быть не в этом файле, а в спец для польз. виджетов:
Здесь временно:

class PrettyWidget(forms.TextInput): # subject = TextField(widget=PrettyWidget)
    class Media:
        css = {
            'all': ('pretty.css',)
        }
"""