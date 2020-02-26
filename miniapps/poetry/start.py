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

# import redis
import pika

def main():

    #params = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection()                                # by default 127.0.0.1:5672
    channel = connection.channel()
    channel.basic_publish(exchange='test', routing_key='test',
                          body=b'Test message.')
    connection.close()

if __name__ == '__main__':
    main()
