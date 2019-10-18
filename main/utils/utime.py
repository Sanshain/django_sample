# -*- coding: utf-8 -*-

import pytz

from django.utils import timezone
from datetime import datetime

class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()

def present_time():
##    return datetime.now()
    return datetime.now()
    return datetime.now().replace(tzinfo=timezone.utc)
