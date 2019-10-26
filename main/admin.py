# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from pytils import translit



from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin

from django.forms import inlineformset_factory
from django.forms import BaseInlineFormSet

from django.utils.translation import ugettext_lazy

from django.db import models

#from main.widgets import RichTextEditorWidget


# Register your models here.


from .models import Profile, Raiting, INote, Comment, Article, Mark, Friends
from .forms import RatingForm
from .forms.user2 import CreatePerson
from .forms.common import ViewImageField, CustomImageField
from .widgets import AdminImageWidget

#class _Field:


#@admin.register(Author, Reader, Editor, site=custom_admin_site)



class CustomInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super(CustomInlineFormSet, self).clean()
        #self.forms
        # example custom validation across forms in the formset
        for form in self.forms:
            # your custom formset validation
            pass

    # https://toster.ru/q/443706
    def get_form_kwargs(self, index):
        kwargs = super(CustomInlineFormSet, self).get_form_kwargs(index)
        # print kwargs
        # kwargs['obj'] = self.form_kwargs['obj'][index]
        return kwargs

class AdvancedModelTab(admin.TabularInline):

    def get_fields(self, request, obj=None):
        if self.fields:
            return self.fields
        print '-----------------------------------------------------'
        form = self.get_formset(request, obj, fields=None).form
        form.base_fields['TargetProfile'].initial = 'dsfdfd'

        return list(form.base_fields) + list(self.get_readonly_fields(request, obj))

class RaitingTab(admin.TabularInline):  #StackedInline
    model = Raiting
    #fields = ['Value','Target']                                                            #'Time' - ошибка not editable из-за того, что AutoField
    readonly_fields = ['Value','Target']                                                    #,'Target'
    fk_name = 'From'
    extra = 0
    show_change_link = True
    form = RatingForm

    #formset = inlineformset_factory(Note, Raiting, fields=('Value',), formset=CustomInlineFormSet, fk_name='Target') #fk_name='Target'- если несколько связей

    def queryset(self, request):
        qs = super(MyModelAdmin, self).queryset(request)
        return qs.filter(Target.From==request.user)                                 #если запись создана текущим юзером

        if request.user.is_superuser:
            return qs

"""
class NotesTab(admin.TabularInline):  #StackedInline
    model = Note
    extra = 1
    show_change_link = True
    can_delete = False
    readonly_fields = ['Content',]

    #RaitingSet = inlineformset_factory(Note, Raiting, fields=('Value',), formset=CustomInlineFormSet, fk_name='Target') #fk_name='Target'- если несколько связей
"""

class CommentsTab(admin.TabularInline):
    model = Comment
    extra = 1
    show_change_link = True
    can_delete = False
    #readonly_fields = ['Content',]

class ArticlesTab(admin.TabularInline):
    fields=('Title', 'Category', 'Content')

    model = Article
    extra = 1
    can_delete = False
    show_change_link = False

class NewAdmin(admin.ModelAdmin):

    class Media:
        css = {
            "all": []
        }
        js = []

    #поля:
    """
    fields = (
        ('City','Age'),
        'Sex',
        'Image'
    )
    """

    fieldsets = (
        (None, {
            'fields': (('first_name','last_name'),'City','Age','Image')
        }),
        (u'Дополнительные поля', {                                                              #только для
            'classes': ('collapse',),
            'fields': ('Sex', 'Image')
        }),
    )

    list_display = (
        'first_name', 'last_name', 'City', '_status', 'date_joined')                     #('Profile',) #'_status',   , lambda r: r.first_name

    inlines = [RaitingTab, CommentsTab, ArticlesTab]
    readonly_fields = ['Sex',]
    list_filter = ['Age', 'City']
    list_display_links = ('first_name',)
    search_fields = ('first_name', 'last_name', 'City',)                          # ['foreign_key__related_fieldname']

    exclude = ('code',)
    formfield_overrides = {
        models.ImageField : {'widget' : AdminImageWidget}
        #models.TextField: {'widget': RichTextEditorWidget},
    }
    #form = CreatePerson                                                            #ошибка на e-mail

    def save_model(self, request, obj, form, change):
        # происходит при сохранении модели

        #obj.code = translit.slugify(obj.title)
        obj.save()

    def __init__(self, *args, **kwargs):

        super(NewAdmin, self).__init__(*args, **kwargs)

        # self.form['Image'] = CustomImageField(label=self.fields['Image'].label)   #ошибка
        #self.list_display_links = (None, )


    #отображать только друзей
    def get_queryset(self, request):

        qs = super(NewAdmin, self).get_queryset (request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)                                       #friend




    #def _first_name_display(self, obj): return obj.first_name
    def _status(self, request): return request.first_name                           #u'<a href="#">Вернуть комиссию</a>'

    #_first_name_display.short_description = 'my_title_in_admin'

    _status.short_description = u'Статус'
    _status.allow_tags = True



admin.site.register(Profile)          #admin.site.register(Profile)   NewAdmin
admin.site.register(Comment)
admin.site.register(Mark)



#admin.site.register(Note)                      #абстрактная модель не может быть зарегистрирована в admin
