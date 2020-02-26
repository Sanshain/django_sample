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



sock = socket.socket()
sock.connect(('localhost', 9091))


sock.send(b"Hello!\n")


data = sock.recv(1024)
print data


sock.close()



