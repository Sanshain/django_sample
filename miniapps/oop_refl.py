# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      комп
#
# Created:     23.02.2019
# Copyright:   (c) комп 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from abc import ABCMeta, abstractmethod, abstractproperty

class InterfaceMetaclass(type):

    def __new__(i_metaclass, class_name, class_parents, class_attr):

        class_attr['isInterface'] = False
        if class_name[0] == 'I' and class_name[1].isupper():
            class_attr['isInterface'] = True

        return type(class_name, class_parents, class_attr)

class Interface(object):
    __metaclass__ = InterfaceMetaclass

print Interface.isInterface



class DjangoInterface(object):


    @classmethod
    def isInterface(cls):
        return cls.__name__[0] == 'I' and cls.__name__[1].isupper()

    isInterface = False

    def __init__(self):
        print self.isInterface

    def __new__(cls, *args, **kwargs):
        obj = super(DjangoInterface, cls).__new__(cls)

        name = cls.__name__

        if (len(name) < 2): return obj


        if cls.__name__[0] == 'I' and cls.__name__[1].isupper():
            raise Exception(cls.__name__ + ' is abstract class or interdace')
            #obj.isInterface = True
        return obj

class ID(DjangoInterface):
    pass

#c = DjangoInterface()
#d = ID()


class A(object):
    def F(self):
        print type(self).__name__

A().F()

def main():
    pass

if __name__ == '__main__':
    main()




