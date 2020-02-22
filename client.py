#!/usr/bin/python2

from threading import Thread
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 13579,))


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

while True:
    message = raw_input()
    sock.sendall(message)
