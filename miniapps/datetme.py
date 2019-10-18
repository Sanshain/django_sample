#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      комп
#
# Created:     17.02.2019
# Copyright:   (c) комп 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import datetime


def main():
    a = datetime.datetime.now()        #datetime(2014, 2, 3, 18, 18, 42, 66853)
    b = datetime.datetime(2014, 3, 3, 18, 18, 54, 49846)
    print a.date()
    print b - a
    print datetime.timedelta(0, 11, 982993)

if __name__ == '__main__':
    main()
