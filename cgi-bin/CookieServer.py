#CookieServer.py

from socket import socket, AF_INET, SOCK_STREAM #, SOL_SOCKET, SO_REUSEADDR
import os.path
from os import path
import random

#Create a TCP socket 
#Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)
#serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverPort=2063
# Assign IP address and port number to socket
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ("Interrupt with CTRL-C")

cookie_recipes = ["Chocolate Chip", "Gingerbread", "Snickerdoodle", "White Chocolate Macadamia Nut", "Sugar", "Shortbread"]
milks = ["Plain", "Chocolate", "Strawberry", "Soy", "Almond"]

while True:
	try:
            connectionSocket, addr = serverSocket.accept()
            print ("Connection from %s port %s" % addr)
		# Receive the client packet
            message = connectionSocket.recv(2048).decode()
            print ("Orignal message from client: ", message)

            filename = message.split()[1].partition("/")[2]		

            cookies = message.partition("Cookie: ")[2].partition("\n")[0].split(";")
            for c in cookies:
                c.replace(" ", "")

            http_msg = ""

            if filename == "cookies":
                cookie_str = "<br>".join(cookies)

                http_msg = '''\
<!doctype html>
<html>
        <head>
                <title>Cookie Page</title>
        </head>
        <body>
                <h1>Cookies:<br>{0}</h1>
        </body>
</html>
'''.format(cookie_str)
            else:
                f = open(filename, "r")
                http_msg = f.read()

            random.shuffle(cookie_recipes)
            random.shuffle(milks)

            buffer = '''HTTP/1.1 200 OK\nContent-length: {2}\nContent-type: text/html; charset=utf-8\nSet-Cookie: cookie={0}\nSet-Cookie: milk={1}\n\n'''.format(cookie_recipes[0], milks[0], str(len(http_msg.encode('utf-8'))))
            buffer = buffer + http_msg

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
