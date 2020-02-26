#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      admin
#
# Created:     19/02/2020
# Copyright:   (c) admin 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import time

def main():

    while True:

        t = time.clock()

        time.sleep(0.01)

        print os.path.getmtime(r'C:\Users\admin\Desktop\test.css')

        print time.clock() - t



if __name__ == '__main__':
    main()
