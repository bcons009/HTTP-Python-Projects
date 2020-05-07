from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import os.path
from os import path

def openClientConn(hostname, message):
    serverName = hostname
    serverPort = 80
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    #Add if-modified-since header to message
    message_p = message.parition("\n\n")
    message_p[0] += "If-Modified-Since: Sat, 23 Nov 2019 19:43:31 GMT"
    message = "".join(message_p)

    clientSocket.send(message.encode())
    server_response = clientSocket.recv(2048).decode()
    print ('From Server: ', server_response)
    clientSocket.close()
    return server_response

#Create a TCP socket 
#Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverPort=2063
# Assign IP address and port number to socket
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ("Interrupt with CTRL-C")
while True:
	try:
            connectionSocket, addr = serverSocket.accept()
            print ("Connection from %s port %s" % addr)
		# Receive the client packet
            message = connectionSocket.recv(2048).decode()
            print ("Orignal message from client: ", message)

            buffer = ""
           
            hostname = message.partition("Host: ")[2].partition("\n")[0]
            if hostname == "www.youtube.com" or hostname == "www.bing.com":
                buffer = '''HTTP/1.1 403 Forbidden\nContent-length: 56\nContent-type:text/plain\n\n401\nNo bing or youtube allowed (go read a book or something)'''
            else:
                dirs_file = message.split()[1].partition("/")[2].split("/")
                filename = dirs_file[len(dirs_file) - 1]
                filepath = "proxy-bin/" + hostname
            

                for d in dirs_file:
                    if os.path.exists(d) == False and d != filename:
                        os.makedirs(d)
                    if d != filename:
                        filepath = filepath + "/" + d
                        os.chdir(d)

                dest_msg = openClientConn(hostname, message)
                http_code = dest_msg.partition("HTTP/1.1 ")[2].partition(" ")[0]
                file = dest_msg.partition("\n\n")[2]

                if http_code == "200":
                    f2 = open(filename, "w")
                    f2.write(file)
                    f2.close()
                
                buffer = '''HTTP/1.1 200 OK\nContent-length:''' + str(len(file)) + '''\nLast-Modified: Wed, 16 Oct 2019 19:43:31 GMT\n\n'''
                f1 = open(filename, "r")
                buffer = buffer + f1.read()

                file_dir = True
                for d in dirs_file:
                    if file_dir:
                        file_dir = False
                    else:
                        os.chdir("..")

            connectionSocket.send(buffer.encode())
            
            connectionSocket.close()
	except IOError:
            print ("Not found %s" % filename)
            buffer = '''HTTP/1.1 404 Not Found\nContent-length: 21\nContent-type: text/plain\n\n404\nHuman is Mismatch'''
            connectionSocket.send(buffer.encode())
            connectionSocket.close()
	except KeyboardInterrupt:
            print ("\nInterrupted by CTRL-C")
            break
serverSocket.close()
