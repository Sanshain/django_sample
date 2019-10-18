#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      комп
#
# Created:     02.03.2019
# Copyright:   (c) комп 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class Dummy(object):
    def __getattr__(self, attr):
        return attr.upper()
d = Dummy()
print d.does_not_exist
print d.what_about_this_one

class Fees(object):
    """"""
    def __init__(self):
        """Конструктор"""
        self._fee = None

    def get_fee(self):

        return self._fee

    def set_fee(self, value):
        print "set"
        self._fee = value

    fee = property(get_fee, set_fee)

def main():
    f = Fees()

    f.fee = "2"
    print( f.fee )

if __name__ == '__main__':
    main()
