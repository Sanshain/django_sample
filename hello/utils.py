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

class SockLiaison:

    def __init__(self, host='localhost', port=9091):

        # start node.js:

        self.__compiler_init()
        self.__ = socket.socket()
        self.__.connect((host, port))

    def style_compile(self, pre_style):
        '''
        Compile pre_style in runtime and turn out the result
        '''

        t = clock()

        self.__.send(buffer(pre_style))
        data = self.__.recv(1024)                                                      # 10-15 sec

        print 'received compiled css by size equal to %s during %s ms'%(len(data), clock() - t)

        return data

    def pre_compile(self, pre_style, tgt, o='w'):
        '''
        Compile pre_style to tgt file
        '''
        sock.send(buffer(pre_style))
        data = self._.recv(1024)                                                      # 10-15 sec

        with open(tgt, o) as tgt_file: tgt_file.write('\n' + css)
        print "less compiled to {}".format(tgt)

    def __compiler_init(self):
        os.system("cd ../node-less_connect & start node less_connection")