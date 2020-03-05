# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      admin
#
# Created:     18/02/2020
# Copyright:   (c) admin 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import socket
from time import clock


class NodeLiaison:
    def __init__(self, host='localhost', port=9091):
        self._ = socket.socket()
        self._.connect((host, port))

    def StyleCompile(self, pre_style):
        '''
        Compile pre_style in runtime and turn out the result
        '''

        t = clock()

        sock.send(buffer(pre_style))
        data = self._.recv(1024)                                                      # 10-15 sec

        print 'received compiled css by size equal to %s during %s ms'%(len(data), clock() - t)

        return data

    def PreCompile(self, pre_style, tgt, o='w'):
        '''
        Compile pre_style to tgt file
        '''
        sock.send(buffer(pre_style))
        data = self._.recv(1024)                                                      # 10-15 sec

        with open(tgt, o) as tgt_file: tgt_file.write('\n' + css)
        print "less compiled to {}".format(tgt)









sock = socket.socket()

sock.connect(('localhost', 9091))                                           # 10-15 sec

times = []

while True:

    r = raw_input('Enter code: ')

    if not r:
        break

    t = clock()

    sock.send(buffer(r))

    data = sock.recv(1024)                                                      # 10-15 sec
    print '---'
    print len(data)
    print data
    print sock.fileno()

    delta = clock() - t

    print delta

    times.append(delta)


sock.close()                                                                    # если приложение завершает работу, то можно без этого


print 'average measurement - {:.3} - from {}'.format(sum(times)/len(times), len(times))

