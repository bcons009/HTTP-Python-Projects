#TCPServer.py

from socket import socket, AF_INET, SOCK_STREAM #, SOL_SOCKET, SO_REUSEADDR

#Create a TCP socket 
#Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)
#serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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

            filename = message.split()[1].partition("/")[2]


            langs = ""
	    #this if-statement is only added to keep my server code compatible with my other coding examples
            if filename == "hello.html":
                langs = message.partition("Accept-Language: ")[2].partition("\n")[0].split(",")
            lang_found = False
            for x in langs:
                lang = x.split(";")[0]
                lang.replace(" ", "")
                if lang == "en" or lang == "es" or lang == "fr":
                    filename = filename + "." + lang
                    lang_found = True
                    break
            if lang_found == False:
                #Default to English
                filename = filename + ".en"
		


            buffer = '''HTTP/1.1 200 OK\nContent-length: 186\nContent-type:text/html; charset=utf-8\nLast-Modified: Wed, 16 Oct 2019 19:43:31 GMT\n\n'''
            
            f = open(filename, "r")
            buffer = buffer + f.read()

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
