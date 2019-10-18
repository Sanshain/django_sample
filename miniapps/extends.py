#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      комп
#
# Created:     30.03.2019
# Copyright:   (c) комп 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class A(object):pass

class B(object):
    def __init__(self):

        self.b = 1
        print "BBBBBBBBBBBB"

class C(A,B):
    def __init__(self):
        super(C,self).__init__()
        print "CCCCCCCCCCCC"
        #print self.a
        print self.b


class HTMLMixin(object):

    """
    Обычная модель-форма, но наследуясь от нее, вам не нужно писать в шаблоне теги
        <form>, <input submit>, csrf-токен - все это она сделает автоматически
        а так же добавлит к форме css-класс, если он задан в конструкторе

        Добавил: возможность добавлять атрибут enctype к форме

        \sub в __init__ не должен быть равен 'def': надпись должна быть явно указана в классе формы

        предназначен для всех форм
    """

    def __init__(self, sub = 'def', cssclass = '', *args, **kwargs):                 # request=None,

        super(HTMLMixin, self).__init__(*args, **kwargs)
        print '44444444444444444444444'


        self.request = kwargs.pop('request', None)                                   # kwargs.pop('request', None)
        self.submit = sub
        self.css_class = cssclass
        self.enctype = kwargs.get('enctype','')

    @property
    def cls(self):
        return self.__class__.__name__

    def as_h(self):

        csrf_t = '<p style="color:red">Set csrf in your view /HTMLForm</p>'
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


def main():
    c = HTMLMixin()



if __name__ == '__main__':
    main()
