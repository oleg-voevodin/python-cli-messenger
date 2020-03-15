# -*- coding: utf-8 -*-

from threading import Thread
import socket

server_ip = input('Enter server IP: ')
server_port = int(input('Enter server port: '))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((server_ip, server_port))
    print(f'Connected to server {server_ip}:{server_port}')
except:
    print('Error!')


class ReplyHandler(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        while True:
            reply = sock.recv(1024)
            print(reply)

thread = ReplyHandler()
thread.daemon = True
thread.start()

try:
    while True:
        message = bytes(input('Message: '), 'utf8')
        sock.sendall(message)
except KeyboardInterrupt:
    print('Closing connection..')
    sock.close()
    print('Goodbye!'); exit()
