# -*- coding: utf-8 -*-

import os
from os.path import dirname




import lesscpy
from six import StringIO

# par = lambda pth, edge, n: os.path.dirname(pth) if n

def less_compile(content=None):

    p = os.path.abspath('') +'\\test.less'
    with open(p,'r') as less_src: less_src = less_src.read()


    less_src = re.sub('(((?<!:)//.+)|(/\*[\S\s]+?\*\/))','',less_src)           # убирает комментарии
    content = re.sub(r'url\("([\w\d\.\:\_\-\/]+)"\)', 'url(\1)',less_src)       # убирает кавычки внутри url()

    css = lesscpy.compile(StringIO(content))

    p = os.path.abspath('') +'\\test.css'
    with open(p,'w') as cssfl: cssfl.write(css)


import re

reg = re.compile('([\t ]*)-(frag|unit) "([_\w]+)"')

def main():
    par = lambda d, n=1: par(dirname(d), n-1) if n else (d)

    with open(r'C:\Users\admin\Desktop\About light_react.txt', 'r') as reader: r = reader.read()

    print r+ str(u'\t')                                                         # str
    print r.decode('utf-8')                                                    # type == unicode
    r = r.decode('utf-8')

    with open(r'C:\Users\admin\Desktop\copy light_react.txt', 'w') as w: w.write(r.encode('UTF-8'))


    # root = lambda p, e, n=3: p if os.path.split(p)[-1] == e or n == 0 else root(os.path.dirname(p, e, n-1))

    root = lambda p, e: p if os.path.split(p)[-1] == e else root(os.path.dirname(p), e)

    print '.'.join(('asd',  'asd'))

    cur = os.path.abspath('')
    print cur

    print os.path.split(cur)[-1]
    print root(cur, 'Users')

    v = 'qwertyu'
    print v[2:0]

    rez  = reg.match('   -frag "__dfdfdf" \n  \t-frag "dfd"')
    # print dir(r)

    print rez.start()
    print rez.end()
    print rez.pos
    print rez.endpos

##    for m in rez:

##    print '{}:{} - {}'.format(m.start(), m.end(), m.group())
##        print m.groups()


if __name__ == '__main__':

    import time

    c = time.time()

    main()

    print time.time() - c

    print 'compiled'


