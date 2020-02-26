#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      admin
#
# Created:     21/02/2020
# Copyright:   (c) admin 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import re
from time import clock

def _find_blocks(dct, s, _pattern = re.compile(r'/\*~block (\w+)\*/([\s\S]*?)/\*~\*/')):

    _blocks = _pattern.finditer(s)

    s = re.sub(_pattern, '', s)

    for b in _blocks:

        dct[b.group(1)] = dct.get(b.group(1),'') + '\n' + b.group(2)

    return s

def reverse(url, args=tuple()):
    dct = {
        'to_friend' : '/communities/%s'
    }
    return dct[url]%((args[0]+'/') if len(args) else '')



def main():
    fl = r'D:\_virtualenv_main\django_test\main\templates\main\profile_list_2.haml'

    src = "to_friend = \"{% url \"to_friend\" 0 %}\";"
    with open(fl,'r') as e: s = e.read()

    m = re.search(r'{% url [\'"]{1}(\w+)[\'"]{1}\s?(\d*) %}', src)
    # for m in ms:
    url_name, arg = m.groups()
    print m.start()
    print m.end()
    print m.string
    print m.string[0:m.start()]
    print m.group()
    print m.string[m.end():len(m.string)]
    print m.groups()

    url = reverse(url_name, args=[arg]) if arg else reverse(url_name)
    res = src.replace(m.group(), url, 1)

    print res
    # print s

    # log_fl = r'C:\Users\admin\Desktop\log.txt'
    # reg = r'(?<=\n)([\ \t]+)((%|\.)\w+[\ ])(%\w+)'

    from warnings import warn

    warn('My warning')

    r = re.search(r'(\s|\t)-block linksfffffff', s)                                    # , re.DEBUG
##    print r.groups()[0] + '4'
##    print r.group()



##    with open(log_fl,'w') as p: p.write(s)

    print 'compiled'

    return




if __name__ == '__main__':
    main()
