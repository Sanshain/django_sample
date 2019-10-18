# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      комп
#
# Created:     16.02.2019
# Copyright:   (c) комп 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import zlib
##import pytz
import datetime


str_object1 = open('props.py', 'rb').read()
str_object2 = zlib.compress(str_object1, 9)
f = open('compressed_file', 'wb')
f.write(str_object2)
f.close()

s = ''
for a in range(128):
    if chr(a).encode('utf-8').isdigit():
        s+=chr(a)

print (s)


def main():
##    print pytz.all_timezones_set
    print datetime.datetime.now()


if __name__ == '__main__':
    main()
