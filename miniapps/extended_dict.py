# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      комп
#
# Created:     22.04.2019
# Copyright:   (c) комп 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class AEnum (object):

    _values = {}

    def __new__(cls, *iterable):                                                  # итератор двойных итераторов
        id=1

        for it in iterable:
            AEnum._values[id]=it
            id <<= 1

        return tuple.__new__(cls, AEnum._values.keys())

    def __init__(self, *keys):                                                   # итератор двойных итераторов
        self.values = AEnum._values.copy()
        AEnum._values = {}
        super(AEnum, self).__init__(keys)

    # при запросе несуществующих атрибутов
    def __getattr__(self, attr):
        if attr in self.values.values():
            return 1<<self.values.values().index(attr)                                 # 2**
        else:
            raise Exception('called enum-object has no the attr called'
                            +' \"'+str(attr)+'\" and has no the value named \"'+str(attr)+'\"')

    def __getitem__(self, key):
        if key in self.values.keys():
            return self.values[key]
        else:
            return self.__getattr__(key)

    def __iter__(self):
        for item in self.values.items():
            yield item

    def __str__(self):
        return super(AEnum, self).__repr__()

    def __repr__(self):
        #
        return str(self.__sum__())


    def __sum__(self):
        # выведет сумму индексов
        r = 0
        for i in self.values:
            r |= i
        return r



class Enum (AEnum, tuple):


    def __call__(self, arg):
        lb = []
        i=0
        r=''
        for i in range(len(self)):
            b = (arg >> i) & 1
            lb.append(b)
            if b:
                r += ('|' if len(r) > 0 else '') + self[1<<i]
                #print '{0} for {1}'.format(self[1<<i],i+1)

        #return r
        return _Enum(self, arg)

    def Optional(self, func):
        # специальные требования, или условия для изменения значения
        if callable(func):
            self.optional = func

        return self

"""
    Этот экз-р не должен создаваться явно. Только через Enum
"""
class _Enum(AEnum, list):
    def __new__(cls, *_enum):
        enum, arg = _enum                                                           # итератор двойных итераторов

        if hasattr(enum, 'optional'):
            if enum.optional(arg) == False:
                raise Exception('the condition specified in the "Optional" is not met')

        for i in range(len(enum)):
            b = (arg >> i) & 1
            if b:
                flag = 1<<i
                AEnum._values[flag] = enum[flag]                                    #lb.append((i, enum[1<<i]))
        return list.__new__(cls, AEnum._values.keys())

    def __init__(self, *args):                                                       # итератор двойных итераторов

        enum, arg = args

        self.value = arg                                                            # итератор двойных итераторов
        self.values = {}

        for i in range(len(enum)):
            bit = (arg >> i) & 1
            if bit:
                flag = 1<<i
                self.values[flag] = enum[flag]

        super(_Enum, self).__init__(*self.values.keys())

    def __str__(self):
        for i in self:
            print i
        return super(_Enum, self).__str__()



    def __eq__(self, other):
        if type(other) == str:
            if other in self.values.values():
                return True
            else:
                return False
        elif type(other) == int:
            return self.__sum__() == other
        else:
            return super(_Enum,self).__eq__(other)

    def __call__(self):

        r=''
        for i in self.values:
            r += ('|' if len(r) > 0 else '') + self[i]

        return r


def check(arg):
    if arg & 1 == 0 and (arg>>1) & 1 == 1:
        check.notis = 'Лучший друг не может быть недругом'
        return False
    else: return True

def main():
    #check = lambda a: a & 3 != 2
    print (not 1) + 0
    print 3 & 3

    #e = Enum('first','dfdf','rt').Optional(lambda a: a & 3 != 2)                     #lambda a: a & 3 != 2

    e = Enum('first','dfdf','rt').Optional(lambda a: a & 3 != 2)                     #lambda a: a & 3 != 2

    e = Enum('first','dfdf','rt')

    e.Optional(lambda val: val & (e.first + e.dfdf) != (not e.first) + e.dfdf)
    print e[1]
    print e.first+e.rt
    print e
    el = e(3)
    print el.__sum__()
    print el()
    if el == 'rt':
        print 'ok'

    print ''

    for i in e:
        print i

    print ''

    Enum('second')[1]

    print e['first']
    print e.first





if __name__ == '__main__':
    main()
