#!/usr/bin/python

from socket import socket, SOCK_STREAM, AF_INET
import mod_html
import sys
import os

sys.stderr = sys.stdout

def read_response(socket, code):
	result = ""
	exit_condition = False
	while not exit_condition:
		message = socket.recv(2048).lstrip()
		result += message
		exit_condition = message[0:4] == "{0} ".format(code)
	return result

def expect_code(socket, code):
	recv = read_response(socket, code)
	#print "<===receive: " + recv
	return recv

def send_expect_code(socket, msg, code):
	#print "===>sending: " + msg
	socket.send(msg + "\r\n")
	return expect_code(socket, code)

def read_data(dataSocket):
	result = ""
	msg = "non-empty string"
	while len(msg) > 0:
		msg = dataSocket.recv(2048)
		result += msg
		#print(msg)
	#print "socket closed on other end, closing on this end"
	#dataSocket.shutdown(dataSocket.SHUT_RDWR)
	dataSocket.close()
	return result

def ftp1():
	serverName = 'ftp.cs.fiu.edu'
	serverPort = 21
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName, serverPort))
	expect_code(clientSocket, "220")
	send_expect_code(clientSocket,"USER anonymous","331")
	send_expect_code(clientSocket,"PASS bcons009@fiu.edu","230")
	send_expect_code(clientSocket,"TYPE A","200")
	message = send_expect_code(clientSocket,"PASV","227")
	start = message.find("(")
	end = message.find(")")
	tuple = message[start+1:end].split(',')
	print tuple
	port = int(tuple[4]) * 256 + int(tuple[5])
	print port
	dataSocket = socket(AF_INET, SOCK_STREAM)
	dataSocket.connect((serverName, port))
	send_expect_code(clientSocket,"LIST","150")
		#read below line into html?
	list = read_data(dataSocket)
	expect_code(clientSocket, "226")
	return (list, clientSocket)

def ftp2(list, clientSocket, input):
	results = list.split("\n")
	filename = ""

	#Parse result, splitting by newlines
	for x in results:
		if x.find(input) != -1:
			if x[0] == "d":
				filename = "d_" + input
			else:
				filename = "f_" + input
			break

	if filename[0] == "d":
		filename = filename.partition("_")[2]
		send_expect_code(clientSocket,"CWD " + filename,"150")
		expect_code(clientSocket,"250")
		##send_expect_code(clientSocket,"LIST","150")
		#new_list = read_data(dataSocket)
		#expect_code(clientSocket, "226")
		#return new_list
	elif filename[0] == "f":
		filename = filename.partition("_")[2]
		send_expect_code(clientSocket, "RETR " + filename, "150")
		expect_code(clienSocket, "226")
		#return ""

	send_expect_code(clientSocket, "QUIT", "221")
	clientSocket.close()

def html(list, input):
	
	print '''\
<!doctype html>
<html>
	<head>
		<title> HTML FTP Client</title>
	</head>
	<body>
		<form method="POST" action="">
			<p>
				{0}
			</p>
			<p>
				\nWhich file? <input type="text" name="input" value="{1}">
			</p>
		</form>
	</body>
</html>
'''.format(list, input)

def main():
	print "Content-type: text/html\n"
	input = ""
	parsed = mod_html.parse()
	if 'input' in parsed:
		input = parsed['input']
	list, clientSocket = ftp1()
	html(list, input)
	output = ftp2(list, clientSocket, input)

main()
