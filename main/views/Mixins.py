# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.urlresolvers import resolve


class CSSMixin(object):
    css_path = 'style'

    def get_default_style(self, **kwargs):
        """
        Добавляет в контекст ключ link со списком для хранения наименований подгружаемых файлов css.
        И добавляет туда одноименный файл css, который должен лежать в корне папки /static/

        Его нужно вызвать вручную
        """


        context = {}
        if 'context' in kwargs:
            context = kwargs['context']

        baseurl = settings.STATIC_URL + self.template_name.replace('.html','')
        basepath = os.path.join(settings.BASE_DIR, __package__.split('.')[0], baseurl[1:])

        print basepath+'.css'
        if os.path.exists(basepath+'.css'): context['links'] = [baseurl + '.css']

        return context

    def get_context_data(self, *args, **kwargs):                                    # расширение контекста
        """
        Переопределение get_context_data для включения метода set_css в поток выполнения mro

        Делает то же самое, что get_default_style, но не для одноименного файла, а для
        одноименной папки, лежащей в корне static. Все файлы внутри нее будут автоматически
        подключены в заголовочный файл

        """

        context = super(CSSMixin, self).get_context_data(*args, **kwargs)

        baseurl = settings.STATIC_URL + self.css_path + '/' + self.template_name.replace('.html','')

        if settings.DEBUG:
            baseurl = baseurl.replace('.haml','')

        basepath = os.path.join(settings.BASE_DIR, __package__.split('.')[0], baseurl[1:])

        if os.path.exists(basepath+'.css'):
            context['links'] = [baseurl + '.css']
        else:
            print 'cant find the file {}'.format(basepath+'.css')
            if settings.DEBUG:

                css_file = open(basepath+'.css', "w")
                css_file.write("")
                css_file.close()

                os.system(basepath+'.css')

        if os.path.exists(basepath):
            for css in os.listdir(basepath):
                context['links'].append(os.path.join(baseurl, css))

        self.set_css(context)

        return context

    def set_css(self, context):
        """
        override this for to define custom css-files
        """
        pass