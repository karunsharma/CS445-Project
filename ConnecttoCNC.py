#Author Karun Sharma
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.connect(('192.168.56.101',11111)) #Reference to local server VM

STATUS = 'READY TO ATTACK'

while True:
	data = s.recv(1024)
	if "STATUS" in data:
		s.send(STATUS)
	print("Data receieved: {}".format(data))