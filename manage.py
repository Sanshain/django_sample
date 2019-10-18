# -*- coding: utf-8 -*-
#!/usr/bin/env python
#from __future__ import unicode_literals

import os
import sys

#locale.setlocale(locale.LC_ALL, "") #? - для перевода


if __name__ == "__main__":

    activate_this_file = r"D:\env\Scripts\activate_this.py"

    execfile(activate_this_file, dict(__file__=activate_this_file))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
