#ThreadedServer.py

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
import os.path
from os import path


class WebThreads(Thread):
    def __init__(self, socket, addr):
        Thread.__init__(self)
        self.socket = socket
        self.addr = addr

    def run(self):
        try:
            print ("Connection from %s port %s" % self.addr)
                # Receive the client packet
            message = self.socket.recv(2048).decode()
            print ("Orignal message from client: ", message)

            filename = message.split()[1].partition("/")[2]

            buffer = '''HTTP/1.1 200 OK\nContent-length: 186\nContent-type:text/html; charset=utf-8\nLast-Modified: Wed, 16 Oct 2019 19:43:31 GMT\n\n'''

            f = open(filename, "r")
            buffer = buffer + f.read()

            self.socket.send(buffer.encode())
            self.socket.close()
        except IOError:
            buffer = '''HTTP/1.1 404 Not Found\nContent-length: 21\nContent-type: text/plain\n\n404\nHuman is Mismatch'''
            self.socket.send(buffer.encode())
            self.socket.close()


#Create a TCP socket 
#Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)
#serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverPort=2063
# Assign IP address and port number to socket
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

threads = []

print ("Interrupt with CTRL-C")
while True:
	try:
            connectionSocket, addr = serverSocket.accept()

                #begin threading here

            client_thread = WebThreads(connectionSocket, addr)
            client_thread.start()
            threads.append(client_thread)
	except KeyboardInterrupt:
            for t in threads:
                t.join()
            print ("\nInterrupted by CTRL-C")
            break
serverSocket.close()
