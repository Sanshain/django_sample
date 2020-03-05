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

# less_compile
import lesscpy
from six import StringIO

import re

# NodeLiaison
import socket
from time import clock


def less_compile(less_src, tgt, o='w'):

    less_src = re.sub('(((?<!:)//.+)|(/\*[\S\s]+?\*\/))','', less_src)           # убирает комментари
    # less_src = re.sub(r'url\(([\w\d\.\:\_\-\/]+)\)', 'url("\1")', less_src)      # добавляет кавычки внутри url()

    with open(r'C:\Users\admin\Desktop\test.less', 'w') as p: p.write(less_src)

    css = lesscpy.compile(StringIO(less_src))                                       # minify=True
    # lesscpy.compile(StringIO(u"a { border-width: 2px * 3; }"), minify=True)

    # css = re.sub(r'url\("([\w\d\.\:\_\-\/]+)"\)', 'url(\1)', css)      # убирает кавычки внутри url()

    css = '\n\n' + css

    with open(tgt, o) as tgt_file: tgt_file.write(css)

    print "less compiled to {}".format(tgt)



import os
deep_root = lambda p, e, d=4: (
    p if os.path.split(p)[-1] == e else (
        deep_root(os.path.dirname(p), e, d-1) if d>0 else None
    )
)
deep_split = lambda path, deep = 2: (
    os.path.split(path) if deep == 1 else deep_split(os.path.split(path)[0], deep - 1)
)


class SockLiaison:

    def __init__(self, _type = None, host='localhost', port=9091):

        # start node.js:

        self.__type = _type
        self.__compiler_init()
        self.__ = socket.socket()
        self.__.connect((host, port))

    def code_compile(self, style_code):
        '''
        Compile style_code in runtime and turn out the result

        - expected:
            style_code - raw src code of less(stylus|scss)

        '''


        self.__.send(buffer(style_code))
        data = self.__.recv(1024)                                                      # 10-15 sec



        return data

    def file_compile(self, src_code, tgt, o='w'):
        '''
        Compile src_code to tgt file
        '''

        #tgt = r"D:\_virtualenv_main\django_test\main\static\style\pages\profile_list_2.css"

        t = clock()

        fl_name = os.path.basename(tgt).split('.')[0]
        _remains, _type = deep_split(tgt)
        _src = deep_root(_remains, 'main')
        src_log_file = os.path.join(_src, 'templates', _type, '.'.join((fl_name, self.__type or 'style')))
        with open(src_log_file, 'w') as pen: pen.write(src_code)

        self.__.send(buffer(src_log_file))
        css = self.__.recv(4096)                                                      # 10-15 sec

        with open(tgt, o) as tgt_file: tgt_file.write('\n' + css)
        print 'received and saved compiled css by size equal to %s during %s ms'%(len(css), clock() - t)

    def __compiler_init(self):

        os.system("cd ../node-less_connect & start /min node less_connection")