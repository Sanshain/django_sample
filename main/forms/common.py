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

class ViewImageField(BoundField):
    """
    Кастомный внешний вид для BoundField ImageField:
        Позволяет задавать кастомный css-класс для label и пользовательский текст

    """
    def __init__(self, form, field, name, textvalue = 'textvalue', css_cls = 'upload_image'):
        if textvalue == 'textvalue': textvalue = 'Define ' + textvalue + ' in ' + self.__class__.__name__
        self.text = textvalue
        self.css_class = 'class=' + css_cls

        super(ViewImageField, self).__init__(form, field, name)

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
            contents = format_html(u'<label {}>{} <span {}>{}</span> </label>', attrs, contents, self.css_class, self.text)
        else:
            contents = conditional_escape(contents)
        return mark_safe(contents)

class CustomImageField(ImageField):
    """
	отвечает за представление поля в шаблоне через методы класса BoundField, т.к.
	BoundField - отвечает за представление поля в шаблоне
	Нам надо переопределить label_tag, поэтому возвращаем свой класс BoundField с переопределенным методом label_tag
    """
    def get_bound_field(self, form, field_name):
        return ViewImageField(form, self, field_name, "Выбрать")	#css_cls =

	"""
	в конструкторе добавили поле parent - если он не None, тогда с него берем некоторые заданные параметры
	"""
    def __init__(self,
		parent = None, 	#FileInput
		required=True,
		widget=None,
		label=None,
		initial=None,
        help_text='',
		error_messages=None,
		show_hidden_initial=False,
        validators=(),
		localize=False,
		disabled=False,
		label_suffix=None):

		# если он не None, тогда с него берем некоторые заданные параметры
		if parent:
			label = parent.label
			widget = parent.widget
			self.textvalue = ''

		# так же надо задать некоторые параметры для label

		super(CustomImageField, self).__init__(
				required,
				widget,
				label,
				initial,
				help_text,
				error_messages,
				show_hidden_initial,
				validators,
				localize,
				disabled,
				label_suffix)

class HTMLMixin(object):

    """
    Обычная модель-форма, но наследуясь от нее, вам не нужно писать в шаблоне теги
        <form>, <input submit>, csrf-токен - все это она сделает автоматически
        а так же добавлит к форме css-класс, если он задан в конструкторе

        Добавил: возможность добавлять атрибут enctype к форме

        \sub в __init__ не должен быть равен 'def': надпись должна быть явно указана в классе формы

        предназначен для всех форм
    """



    def __init__(self, submit = 'no', cssclass = '', tag = 'div', *args, **kwargs):                 # request=None,

        super(HTMLMixin, self).__init__(*args, **kwargs)

        self.request = kwargs.pop('request', None)                                   # kwargs.pop('request', None)
        self.tag = tag
        self.submit = submit
        self.css_class = cssclass
        self.enctype = kwargs.get('enctype','')

    @property
    def cls(self):
        return self.__class__.__name__

    def __unicode__(self):
        return self.as_h()

    def as_h(self):
        """
        Делает help_text_html невидимым и добавляет к нему класс help-text
        """
        as_p = self._html_output(
            normal_row = u'<'+self.tag+'%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</'+self.tag+'>',
            error_row = u'<div class="error">%s</div>',
            row_ender = '</div>',
            help_text_html = u'<div hidden class="help-text">%s</div>',
            errors_on_separate_row = False)

        csrf_t = '<p style="color:red">Set csrf in your view</p>'
        submit = 'in_%s_not_defined'%self.cls if self.submit == 'no' else self.submit
        cssclass = format_html(u'class="{}"', self.css_class) if len(self.css_class) > 0 else ''
        enctype = ''                                                                #' enctype={}'.format(self.enctype) if self.enctype else ''

        if self.request != None:
            val = 'input type="hidden" name="csrfmiddlewaretoken" value="'
            csrf_t = '<' + val + get_token(self.request) + '">'

        html = '<form method="post"{0}{1}>{2}'.format(cssclass, enctype, csrf_t)
        html += as_p + '<input type="submit" value=%s></form>'%submit

        return mark_safe(html)



class HTMLForm(forms.ModelForm):

    class Enctype:
        Default = ''
        Multipart = 'multipart/form-data'
        Text = 'text/plain'

        def __str__(self):
            return self.value

        def __init__(self, value=''):
            self.value = value


    """
    Обычная модель-форма, но наследуясь от нее, вам не нужно писать в шаблоне теги
        <form>, <input submit>, csrf-токен - все это она сделает автоматически
        а так же добавлит к форме css-класс, если он задан в конструкторе

        Добавил: возможность добавлять атрибут enctype к форме

        \sub в __init__ не должен быть равен 'def': надпись должна быть явно указана в классе формы
        предназначен только для ModelForm, не предназначен для обычных форм
    """

    def __init__(self, sub = 'def', cssclass = '', *args, **kwargs):                 # request=None,

        super(HTMLForm, self).__init__(*args, **kwargs)

        self.request = kwargs.pop('request', None)                                   # kwargs.pop('request', None)
        self.submit = sub
        self.css_class = cssclass
        self.enctype = kwargs.get('enctype','')

    @property
    def cls(self):
        return self.__class__.__name__

    def as_h(self):

        csrf_t = '<p style="color:red">Set csrf in your view \%s\</p>'%self.cls
        cssclass = format_html(u' class="{}"', self.css_class) if len(self.css_class) else ''
        enctype = ' enctype={}'.format(self.enctype) if self.enctype else ''
        submit = 'in %s not defined'%self.cls if self.submit == 'def' else self.submit

        if self.request:
			csrf_t = '<input type="hidden" name="csrfmiddlewaretoken" value="' + get_token(self.request) + '">'

        html = '<form method="post"{0}{1}>{2}'.format(cssclass, enctype, csrf_t)
        html += self.as_p() + '<input type="submit" value=%s></form>'%submit

        return mark_safe(html)

    def __unicode__(self):
        return self.as_h()



class HTMLabelForm(HTMLForm):
    """
    то же самое, что и HTMLForm, но позволяет вручную указывать тэг


    """

	# хорошо бы перенести в конструктор. Но почему не работает через эксземпляр класса так, так же непонятно. Надо пост запостить:
    tag = 'div'
    """
    Делает help_text_html невидимым и добавляет к нему класс help-text
    """
    def as_h(self):

        as_p = self._html_output(
            normal_row = u'<'+HTMLabelForm.tag+'%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</'+HTMLabelForm.tag+'>',
            error_row = u'<div class="error">%s</div>',
            row_ender = '</div>',
            help_text_html = u'<div hidden class="help-text">%s</div>',
            errors_on_separate_row = False)

        csrf_t = '<p style="color:red">Set csrf in your view</p>'
        submit = self.submit
        cssclass = format_html(u'class="{}"', self.css_class) if len(self.css_class) > 0 else ''

        if self.request != None:
            csrf_t = '<input type="hidden" name="csrfmiddlewaretoken" value="' + get_token(self.request) + '">'
        if self.submit == 'def':
        	submit = 'in_' + self.__class__.__name__ + '_notdefined'

        html = '<form method="post" '+ cssclass + '>' + csrf_t + as_p + '<input type="submit" value=' + submit + '></form>'

        return mark_safe(html)


