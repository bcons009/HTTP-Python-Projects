#UDPClient.py

import select

from socket import socket, SOCK_DGRAM, AF_INET

serverName = 'localhost'
serverPort = 2063
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = "ping"

for x in range(10):
	dropped = True
	clientSocket.sendto(message.encode(), (serverName, serverPort))
	
	clientSocket.setblocking(0)
	ready = select.select([clientSocket], [], [], 1.0)
	if ready[0]:
		modifiedMessage, addr = clientSocket.recvfrom(2048)
		dropped = False
	if dropped:
		print ("Ping {0} dropped".format(x))
	else:
		print (modifiedMessage)
clientSocket.close()
