# -*- coding: utf-8 -*-

from threading import Thread
from datetime import datetime
import socket

maximum_peers = int(input('Enter quantity of maximum connected peers: '))
sock, peers = None, {}

server_port = int(input('Enter server port: '))

class Messenger(object):
    def __init__(self):
        self.setup()
        for i in range(maximum_peers):
            thread = Messenger.Connection()
            thread.daemon = True
            thread.start()

    def setup(self):
        global sock; sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', server_port))
        sock.listen(maximum_peers)

    def send_message(self, message):
        for peer in peers:
            peers[peer].sendall(str(message))

    class Connection(Thread):
        def __init__(self):
            Thread.__init__(self)
        def run(self):
            peer, addr = sock.accept()
            if len(peers) == maximum_peers:
                peers[peer].sendall(b'Can\'t connect to server: maximum peers already connected.')
                peers[peer].close()
            nickname = input('Enter you nickname: ')
            peers[nickname] = peer
            print('Conneted new user from IP: ', addr)
            while True:
                message = peer.recv(1024)
                print(str(message))
                for other in peers:
                    if peer != peers[other]:
                        other.sendall(bytes(f'[{datetime.now().time().strftime("%H:%M:%S")}] {other}: {str(message)}', 'utf8'))

messenger = Messenger()

try:
    while True:
        message = bytes(input('Send message to all users: '), 'utf8')
        messenger.send_message(message)
        
except KeyboardInterrupt:
    sock.close()
    for peer in peers:
        peers[peer].close()
