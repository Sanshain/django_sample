#-------------------------------------------------------------------------------
# Name:        module3
# Purpose:
#
# Author:      admin
#
# Created:     16/02/2020
# Copyright:   (c) admin 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from subprocess import Popen, PIPE, STDOUT
import os
import sys

from time import time, sleep

def main():

    s = r'node D:\_virtualenv_main\just_less_2.js' + '\n'
##    p = Popen(['node',r'D:\_virtualenv_main\just_less_2.js'], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
##    p = Popen(['cmd'], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)


    p = Popen(['node',r'D:\_virtualenv_main\just_less_2.js'], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)

    t = time()



##    p.stdin.write(r'C:\Users\admin\Desktop\test.less'+'\n')
##
##    p.stdin.close()                                                           # а быстро ли выполнится это, не измерить
##
##    print p.stdout.read().decode('cp866')                                     # видимо, эта операция все тормозит (join)

##    os.system(s)

    print time() - t

#1       это прсто в поток python(:

##    sys.stdin.write('node')
##    print sys.stdout.readline()




#2
#   pзакрывает соединение
##    p = Popen(["cmd"], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)

##    out, err = p.communicate( 'ping 192.168.1.1\n' )
##
##    print out.decode('cp866')

#3    p = Popen(["cmd"], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)

# мало того, что нет обр свяи, так еще и асинхронно
##    input()
##
##    p.stdin.write('ping 192.168.1.1\n')
##    print 'ping'
##
##    cmd = raw_input('next cmd command: ')
##    p.stdin.write(cmd + '\n')
##    print 'started 1'
##
##    cmd = raw_input('next cmd command: ')
##    p.stdin.write(cmd + '\n')
##    print 'started 2'

#4    p = Popen(["cmd"], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)

# не открывает затем поток на запись
##    cmds = ['1+2\n','ping 192.168.1.1\n']  #
##
##    for cmd in cmds:
##        p.stdin.write(cmd + "\n")
##    p.stdin.close()
##
##    print p.stdout.read().decode('cp866')


##    p.stdin.write(cmd + "\n")

#4
# зависает
##    while True:
##        a = (proc.stdout.readline())
##        if not a: break
##        else:
##            print a.decode('cp866')
##
##    proc.stdin.write('ping 192.168.1.1'+'\n')

##    while True:
##        a = (proc.stdout.readline())
##        if not a: break
##        else:
##            print a

##    proc.kill()

if __name__ == '__main__':
    main()


##    stdin, stdout = os.popen2("node")
##
##    print stdin.write('1+2')
##    print stdout.read()


