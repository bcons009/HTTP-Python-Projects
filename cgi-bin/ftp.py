from socket import socket, SOCK_STREAM, AF_INET

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
	print "<===receive: " + recv
	return recv

def send_expect_code(socket, msg, code):
	print "===>sending: " + msg
	socket.send(msg + "\r\n")
	return expect_code(socket, code)

def read_data(dataSocket):
	result = ""
	msg = "non-empty string"
	while len(msg) > 0:
		msg = dataSocket.recv(2048)
		result += msg
		print(msg)
	print "socket closed on other end, closing on this end"
	dataSocket.shutdown(SHUT_RDWR)
	dataSocket.close()
	return result

def ftp():
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
	read_data(dataSocket)
	expect_code(clientSocket, "226")
	send_expect_code(clientSocket, "QUIT", "221")
	clientSocket.shutdown(SHUT_RDWR)
	clientSocket.close()

def html(list, input):
	
	print'''\
<!doctype html>
<html>
	<head>
		<title> HTML FTP Client</title>
	</head>
	<body>
		<p>
			{0}
		</p>
		<p>
			Which file? <input type="text" name
