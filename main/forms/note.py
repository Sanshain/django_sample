# -*- coding: utf-8 -*-

from django import forms

from ..models import Raiting, Article
from main.widgets import EmptyWidget
from .common import HTMLabelForm

class RatingForm(forms.ModelForm):
    """

    """
    TargetProfile = forms.SlugField(label='Автор',
        initial='___',
        widget = EmptyWidget,
        required=False
    )                                                                                #,widget = EmptyWidget

    error_css_class = 'error_class'                                                  # ошибки валидации???????

    class Meta(object):

        model = Raiting
        fields =  ('Value', 'Target') 		                                         #'Time', - not editable

        labels = {
            'Value': 'Оценка',
            'Target': 'К записи',
        }
        help_texts = {
            'Value': ('Изменить значение'),
        }
        widgets = {
            'TargetProfile': EmptyWidget()
        }
        error_messages = {

        }


    def __init__(self, *args, **kwargs):

        if kwargs.__contains__(u'instance'):                                             #скорее всего для python3 другое...
            if kwargs[u'instance']:
                kwargs.update(initial={
                    # 'field': 'value'
                    'TargetProfile': kwargs[u'instance'].Target.From                     # переопределит get_fields в TabularInline
                })
                #print kwargs[u'instance'].Target.From

            #print kwargs[u'instance']

        super(RatingForm, self).__init__(*args, **kwargs)

        self.submit = u'Оценить'
        self.css_class = ''




class create_note(HTMLabelForm):
    """

    """                                                                             #,widget = EmptyWidget

    error_css_class = 'error_class'                                                  # ошибки валидации???????

    class Meta(object):

        model = Article
        fields =  ('Title', 'Content') 		                                         #'Time', - not editable


        labels = {
            'Title': '',
            'Content':''
        }
        widgets = {
            'Title': forms.TextInput(attrs={'placeholder':u'заголовок', 'style':
                '''


                ''',
                'oninput' : 'window.flag = true;'
                }
            ),
            'Content': forms.Textarea(attrs={'placeholder':u'содержимое', 'style':
                '''

                ''',
                'oninput' :
                '''

                    var title = document.querySelector('#id_Title');

                    if ((title.value.length == 0 || (!window.flag && title.value.length < 35)) &&
                        document.querySelector('#id_Content').value.indexOf('<') < 0)
                    {
                        document.querySelector('#id_Title').value = event.target.value + '...';
                        if (document.querySelector('#id_Title').value.length > 25)
                        {
                            //document.querySelector('#id_Title').style.fontSize = 'large';
                        }
                    }
                '''
                }
            ),
        }

    def __init__(self, *args, **kwargs):
      super(create_note, self).__init__(*args, **kwargs)
      self.submit = u'my_submit'
      self.css_class = 'new_note'



    def save(self, commit=True):
        note = super(create_note, self).save(commit=False)
        note.From = self.user
        print '-----------'
        if commit:
            note.save()
        return note
