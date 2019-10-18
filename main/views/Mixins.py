# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.urlresolvers import resolve


class CSSMixin(object):


    def get_context_data(self, *args, **kwargs):                                    # расширение контекста
        context = super(CSSMixin, self).get_context_data(*args, **kwargs)

        baseurl = settings.STATIC_URL + self.template_name.replace('.html','')
        basepath = os.path.join(settings.BASE_DIR, __package__.split('.')[0], baseurl[1:])

        if os.path.exists(basepath+'.css'): context['links'] = [baseurl + '.css']
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