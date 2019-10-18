#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      комп
#
# Created:     14.09.2019
# Copyright:   (c) комп 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    d = {1:'dfd','rt':'123'}
##    print d.pop('rt')
    s = 'Hello world'
    t = buffer(s, 6, 5)
    print type(t)
    t+='f'
    print type(t)
    print dir(t)
    b=bytearray(b'hello world!')

    print type(b)
    print b
    b+='g'
    print type(b)
    print b

    v = memoryview(b'abcefg')
    print v

    a='asd'
    print a.rjust(5,u'0')

if __name__ == '__main__':
    main()
