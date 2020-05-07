#!/usr/bin/python

import mod_html
import sys
import os
import socket
import time

sys.stderr = sys.stdout

def html(method, send_n, send_s, recv_n, recv_s, subj, msg):
	print '''\
<!doctype html>
<html>
	<head>
		<title>HTML Mail Client</title>
	</head>
	<body>
		<h1>Hello {0}</h1>
		<h2>Method = {1}</h2>
		<h3>Server = {2}</h3>
	<p>
		<form method="{1}" action="">
			<p>
			Sender Name: <input type="text" name="sender_name" value1="{0}">
			</p>
			<p>
			Sender Server: <input type="text" name="sender_server" value2="{2}">
			</p>
			<p>
			Receiver Name: <input type="text" name="receiver_name" value3="{3}">
			</p>
			<p>
			Receiver Server: <input type="text" name="receiver_server" value4="{4}">
			</p>
			<p>
			Subject: <input type="text" name="subject" value5="{5}">
			</p>
			<p>
			Message: <input type="text" name="message" value6="{6}">
			</p>
			<p>
			<input type="submit" value="Send Email">
			</p>
		</form>
	</p>
	</body>
</html>
'''.format(send_n, method, send_s, recv_n, recv_s, subj, msg)

def send_recv(socket, msg, code):
    if msg != None:
        print "Sending==> ", msg
        socket.send(msg + '\r\n')

    recv = socket.recv(1024)
    print "<==Received:\n", recv
    if recv[:3]!=code:
        print '%s reply not received from server.' % code
    return recv

def send(socket, msg):
    print "Sending ==> ", msg
    socket.send(msg + '\r\n')

serverName = 'smtp.cis.fiu.edu'
serverPort = 25

def mail_s(u_name, u_server, t_name, t_server, subj, msg):
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect((serverName, serverPort))
	recv=send_recv(clientSocket, None, '220')

	clientName = ""
	userName = ""
	userServer = ""
	toName = ""
	toServer = ""
	
	clientName = u_name
	userName=u_name
	userServer=u_server
	toName=t_name
	toServer=t_server
	#Send HELO command and print server response.
	heloCommand='EHLO %s' % clientName
	recvFrom = send_recv(clientSocket, heloCommand, '250')
	#Send MAIL FROM command and print server response.
	fromCommand='MAIL FROM: <%s@%s>' % (userName, userServer)
	recvFrom = send_recv(clientSocket, fromCommand, '250')
	#Send RCPT TO command and print server response.
	rcptCommand='RCPT TO: <%s@%s>' % (toName, toServer)
	recvRcpt = send_recv(clientSocket, rcptCommand, '250')
	#Send DATA command and print server response.
	dataCommand='DATA'
	dataRcpt = send_recv(clientSocket, dataCommand, '354')
	#Send message data.
	send(clientSocket, "Date: %s" % time.strftime("%a, %d %b %Y %H:%M:%S -0400", time.localtime()));
	send(clientSocket, "From: %s@%s" % (userName, userServer));
	send(clientSocket, "Subject: %s" % subj);
	send(clientSocket, "To: %s@%s" % (toName, toServer));
	send(clientSocket, ""); #End of headers
	send(clientSocket, "%s" % msg);
	#Message ends with a single period.
	send_recv(clientSocket, ".", '250');
	#Send QUIT command and get server response.
	quitCommand='QUIT'
	quitRcpt = send_recv(clientSocket, quitCommand, '221')

def main():
	print "Content-type: text/html\n"
	send_n = ""
	send_s = ""
	recv_n = ""
	recv_s = ""
	subj = ""
	msg = ""
	parsed = mod_html.parse()
	if 'sender_name' in parsed:
		send_n = parsed['sender_name']
	if 'sender_server' in parsed:
		send_s = parsed['sender_server']
	if 'receiver_name' in parsed:
		recv_n = parsed['receiver_name']
	if 'receiver_server' in parsed:
		recv_s = parsed['receiver_server']
	if 'subject' in parsed:
		subj = parsed['subject']
	if 'message' in parsed:
		msg = parsed['message']
	html("POST", send_n, send_s, recv_n, recv_s, subj, msg)
	if send_n != "" and send_s != "" and recv_n != "" and recv_s != "" and subj != "" and msg != "":
		mail_s(send_n, send_s, recv_n, recv_s, subj, msg)

main()
