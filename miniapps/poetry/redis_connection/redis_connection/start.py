#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      admin
#
# Created:     17/02/2020
# Copyright:   (c) admin 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import redis

def main():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')
    print r.get('foo')

if __name__ == '__main__':
    main()
