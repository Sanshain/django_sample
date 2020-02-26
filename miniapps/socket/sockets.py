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

##def send():
##    sock = socket.socket()
##    sock.bind( ("", 9090) )
##    sock.listen(1)
##    conn, addr = sock.accept()
##    conn.send(b"Hello!\n")
##    conn.close()


def wait():
    sock = socket.socket()
    sock.bind( ("localhost", 9091) )
    sock.listen(5)
    print 'sock.accept'
    conn, addr = sock.accept()
    print 'sock.accepted'

    print conn.gettimeout()
    conn.settimeout(60)                                                         # для длительного ожидания данных (60 sec)

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print str(data)
        conn.send(buffer('recivied '+str(len(data))))

    # data = conn.recv(1024)
    # udata = data.decode("utf-8")
    print str(data)
    conn.close()

if __name__ == '__main__':
    wait()
    # wait()



