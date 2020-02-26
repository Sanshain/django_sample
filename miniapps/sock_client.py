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
    print len(data)
    print data

    delta = clock() - t

    print delta

    times.append(delta)


sock.close()                                                                    # если приложение завершает работу, то можно без этого



print 'average measurement - {:.3} - from {}'.format(sum(times)/len(times), len(times))

