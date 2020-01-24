#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      admin
#
# Created:     24/01/2020
# Copyright:   (c) admin 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class A(object):

    def __init__(self):
        print 0

    def methoda(self, i):
        print 456
        return 1


class B(A):

    def __init__(self):
        pass

    def methoda(self, i):
        a = super(B, self).methoda(3)
##        print 2

def main():
    b = B()
    print b.methoda(1)



if __name__ == '__main__':
    main()
