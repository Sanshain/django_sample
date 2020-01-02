# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.urlresolvers import resolve

from django.template.loader import render_to_string


def _get_file_info (base_path, name, ext = None):

    baseurl = settings.STATIC_URL + base_path + '/' + name.replace('.html','')
    basepath = os.path.join(settings.BASE_DIR, __package__.split('.')[0], baseurl[1:])
    existence = os.path.exists(basepath + '.' + ext if ext else base_path)

    return (existence, baseurl)



class CSSMixin(object):
    css_path = 'style'

    def get_default_style(self, *args, **kwargs):
        """
        Добавляет в контекст ключ link со списком для хранения наименований подгружаемых файлов css.
        И добавляет туда одноименный файл css, который должен лежать в корне папки /static/

        Его нужно вызвать вручную
        """


        context = {}
        if 'context' in kwargs:
            context = kwargs['context']

        baseurl = settings.STATIC_URL + self.css_path + '/' + self.template_name.replace('.html','')

        if settings.DEBUG:
            baseurl = baseurl.replace('.haml','')

        basepath = os.path.join(settings.BASE_DIR, __package__.split('.')[0], baseurl[1:])

        print basepath+'.css'
        if os.path.exists(basepath+'.css'):
            if 'post' in args: context['dynamic_link'] = baseurl + '.css'
            else: context['links'] = [baseurl + '.css']


        return context

    def get_context_data(self, *args, **kwargs):                                    # расширение контекста
        """
        Переопределение get_context_data для включения метода set_css в поток выполнения mro

        Делает то же самое, что get_default_style, но не для одноименного файла, а для
        одноименной папки, лежащей в корне static. Все файлы внутри нее будут автоматически
        подключены в заголовочный файл

        """
        tn = self.template_name


        context = super(CSSMixin, self).get_context_data(*args, **kwargs)

        template_name = tn if tn.find('/') < 0 else tn.split('/')[1]

        baseurl = settings.STATIC_URL + self.css_path + '/' + template_name.replace('.html','')

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
        self._set_css(context)

        return context

    def set_css(self, context):
        """
        override this for to define custom css-files
        """
        pass

    def _set_css(self, context):
        """
        override this for to define custom css-files
        """
        pass



def dynjs_insertion(name, context = {}, path = 'js'):

    availible, baseurl = _get_file_info(path, name)
    context.update({'dynamic_c'+name : baseurl} if availible else {})           # dynamic_c

    return context








def render_fragment(args):

    #template_name, context, surround = args

    request = args[1].pop('request', None)                                     # извлекаем request из 2-го аргумента

    templ = ''

    try:

        templ = render_to_string(
            'fragments/%s%s'%(args[0], '' if '.' in args[0] else '.haml'),
            context=args[1],
            request=request
        ).strip().replace('\t','')                                                         # .replace('\t','') - для оптимизации

    except:

        templ = render_to_string(
            'fragments/%s%s'%(args[0], '' if '.' in args[0] else '.html'),
            context=args[1],
            request=request
        ).strip().replace('\t','')


    if len(args) == 3:
        surround = args[2]                                                     # кортеж из класса и id элемента

        if len(surround) == 2:
            if surround[0]: return u"<div class='{}' id='{}'>{}</div>".format(*(surround + (templ,)))
            else: return u"<div id='{}'>{}</div>".format(surround[1], templ)
        elif len(surround) == 1:
            return u"<div class='{}'>{}</div>".format(*(surround + (templ,)))


    else:
        return templ

def render_root_fragment(templates):

    blocks = []
    for tmpl in templates:
        blocks.append(render_fragment(tmpl) if type(tmpl) is list else tmpl)


    return u'{}{}{}{}{}{}'.format(
        "<div id='main'>",blocks[0],'</div>',
        "<div id='section'>", blocks[1] ,"</div>")



class ReactMixin(object):

    """
        Sample for `args`:

        args = ["articles_main", {
            'articles':articles,
            'request' :self.request }, (
                'articles', 'articles_block')] # - id, class
    """
    _render_fragment = lambda self, args: render_fragment(args)
    _render_root_fragment = lambda self, args: render_root_fragment(args)

    def _get_model_fields(self, args):
        """
        virtual
        """
        raise Exception('Must be overriden')                                    # see ProfileView for example



class LightReact(object):

    @staticmethod
    def RenderFragment(args):
        return render_fragment(args)

    @staticmethod
    def render_root_fragment(tmplts):
        return render_root_fragment(tmplts)
