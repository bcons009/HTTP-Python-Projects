#!/usr/bin/python

import mod_html
import sys
import os
import socket
import time
import base64
import ssl

sys.stderr = sys.stdout

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

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
recv=send_recv(clientSocket, None, '220')

u_name = "bcons009_smtp"
u_server = "outlook.com"
u_pass = "this isn't my actual password for this email account"
t_name = "bcons009_smtp"
t_server = "outlook.com"
subj = "test"
msg = "wassup"

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
send_recv(scc, ".", '250');
#Send QUIT command and get server response.
quitCommand='QUIT'
quitRcpt = send_recv(scc, quitCommand, '221')
