import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect(('192.168.56.101',1111)) #Reference to local server VM