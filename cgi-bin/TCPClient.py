#TCPClient.py

from socket import socket, AF_INET, SOCK_STREAM
serverName = 'ocelot.aul.fiu.edu:2063'
serverPort = 2063
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
message = "it's so cooooool!!!"
clientSocket.send(message.encode())
modifiedMessage = clientSocket.recv(2048).decode()
print ('From Server: ', modifiedMessage)
clientSocket.close()
