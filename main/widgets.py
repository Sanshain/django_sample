from django import forms
from django.forms.widgets import Widget


from django.template import loader
from django.utils.safestring import mark_safe
from django.conf import settings



class AdminImageWidget(forms.FileInput):
    """
    A ImageField Widget for admin that shows a thumbnail.
    http://python.su/forum/topic/9777/
    """

    def __init__(self, attrs={}, *args, **kwargs):

        super(AdminImageWidget, self).__init__(attrs, *args, **kwargs)

    def render(self, name, value, attrs=None):
        url = value.url                                                             # url = settings.SITE_URL + value.url
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s" style="height: 60px;" /></a> '
                           % (url, url)))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))




class EmptyWidget(Widget):
    template_name = 'widgets/empty.html'

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        }}


    def render(self, name, value, attrs=None):
        #print '========================'
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


