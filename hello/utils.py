# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      admin
#
# Created:     26/02/2020
# Copyright:   (c) admin 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import lesscpy
from six import StringIO

# lesscpy.compile(StringIO(u"a { border-width: 2px * 3; }"), minify=True)

import re

def less_compile(less_src, tgt, o='w'):

    less_src = re.sub('(((?<!:)//.+)|(/\*[\S\s]+?\*\/))','', less_src)           # убирает комментари
    # less_src = re.sub(r'url\(([\w\d\.\:\_\-\/]+)\)', 'url("\1")', less_src)      # добавляет кавычки внутри url()

    with open(r'C:\Users\admin\Desktop\test.less', 'w') as p: p.write(less_src)

    css = lesscpy.compile(StringIO(less_src))                                       # minify=True

    # css = re.sub(r'url\("([\w\d\.\:\_\-\/]+)"\)', 'url(\1)', css)      # убирает кавычки внутри url()

    css = '\n\n' + css

    with open(tgt, o) as tgt_file: tgt_file.write(css)

    print "less compiled to {}".format(tgt)