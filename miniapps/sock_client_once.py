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


def main():

    t = clock()

    sock = socket.socket()

    sock.connect(('localhost', 9091))                                           # 10-15 sec

    sock.send(b"Hello!\n")

    data = sock.recv(1024)                                                      # 10-15 sec
    print data


##    sock.close()

    print clock() - t



main()