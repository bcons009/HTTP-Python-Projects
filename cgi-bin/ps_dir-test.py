#TCPServer.py

from socket import socket, AF_INET, SOCK_STREAM #, SOL_SOCKET, SO_REUSEADDR
import os.path
from os import path

filename = "test.txt"

f1 = open(filename, "r")
message = f1.read()
f1.close()

hostname = message.partition("Host: ")[2].partition("\n")[0]
dirs_file = message.split()[1].partition("/")[2].split("/")
filename = dirs_file[len(dirs_file) - 1]
filepath = "proxy-bin/" + hostname

if not os.path.exists(filepath):
    os.makedirs(filepath)
os.chdir(filepath)
print("Filepath = " + os.getcwd())

for d in dirs_file:
    if os.path.exists(d) == False and d != filename:
        os.makedirs(d)
    if d != filename:
        filepath = filepath + "/" + d
        os.chdir(d)

f2 = open(filename, "w")
f2.write("Success!!")
f2.close()

file_dir = True
for d in dirs_file:
    if file_dir:
        file_dir = False
    else:
        os.chdir("..")
