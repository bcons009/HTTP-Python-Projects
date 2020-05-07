#UDPServer.py

import random

from socket import socket, SOCK_DGRAM, AF_INET

#Create a UDP socket 
#Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 2063))
print ("Waiting for connections")
while True:
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(2048)
    # Capitalize the message from the client
    print (message)
    message = message.upper()
    r = random.randrange(0, 5, 1)
    if r != 0:
    	serverSocket.sendto(message, address)
serverSocket.close()
