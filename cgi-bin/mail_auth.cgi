#!/usr/bin/python

import mod_html
import sys
import os
import socket
import time
import base64
import ssl

sys.stderr = sys.stdout

def html(method, send_n, send_s, send_p, recv_n, recv_s, subj, msg):
	print '''\
<!doctype html>
<html>
	<head>
		<title>HTML Mail Client for Authenticated Servers</title>
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
			Sender Password: <input type="password" name="sender_pass" value7="{7}">
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
'''.format(send_n, method, send_s, recv_n, recv_s, subj, msg, send_p)

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

def mail_s(u_name, u_server, u_pass, t_name, t_server, subj, msg):
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect((serverName, serverPort))
	recv=send_recv(clientSocket, None, '220')

	clientName = ""
	userName = ""
	userServer = ""
	toName = ""
	toServer = ""

	user_auth = '%s@%s' % (userName, userServer)
	user64_b = base64.b64encode(user_auth.encode("utf-8"))
	user64 = str(user64_b)
	pass64_b = base64.b64encode(u_pass.encode("utf-8"))
	pass64 = str(pass64_b)
	
	clientName = u_name
	userName=u_name
	userServer=u_server
	toName=t_name
	toServer=t_server
	#Send HELO command and print server response.
	heloCommand='EHLO %s' % clientName
	recvFrom = send_recv(clientSocket, heloCommand, '250')

	#SSL code
	recv = send_recv(clientSocket, 'STARTTLS', '220')
	scc = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

	#put AUTH code here
	authCommand='AUTH LOGIN'
	recvAuth = send_recv(scc, authCommand, '334')
	recvAuth_U = send_recv(scc, user64, '334')
	recvAuth_P = send_recv(scc, pass64, '235')

	#Send MAIL FROM command and print server response.
	fromCommand='MAIL FROM: <%s@%s>' % (userName, userServer)
	recvFrom = send_recv(scc, fromCommand, '250')
	#Send RCPT TO command and print server response.
	rcptCommand='RCPT TO: <%s@%s>' % (toName, toServer)
	recvRcpt = send_recv(scc, rcptCommand, '250')
	#Send DATA command and print server response.
	dataCommand='DATA'
	dataRcpt = send_recv(scc, dataCommand, '354')
	#Send message data.
	send(scc, "Date: %s" % time.strftime("%a, %d %b %Y %H:%M:%S -0400", time.localtime()));
	send(scc, "From: %s@%s" % (userName, userServer));
	send(scc, "Subject: %s" % subj);
	send(scc, "To: %s@%s" % (toName, toServer));
	send(scc, ""); #End of headers
	send(scc, "%s" % msg);
	#Message ends with a single period.
	confirm_send = send_recv(scc, ".", '250');
	#Send QUIT command and get server response.
	quitCommand='QUIT'
	quitRcpt = send_recv(scc, quitCommand, '221')

	if confirm_send.split()[0] == "250":
		print("<br><br><br>Message sent!!")
	else:
		print("Something bad happened to the message...")

def main():
	print "Content-type: text/html\n"
	send_n = ""
	send_s = ""
        send_p = ""
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
	if 'sender_pass' in parsed:
		send_p = parsed['sender_pass']
	html("POST", send_n, send_s, send_p, recv_n, recv_s, subj, msg)
	if send_n != "" and send_s != "" and send_p != "" and recv_n != "" and recv_s != "" and subj != "" and msg != "":
		mail_s(send_n, send_s, send_p, recv_n, recv_s, subj, msg)

main()
