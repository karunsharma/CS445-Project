import socket
import threading

def connectbot():
	pass

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(('',11111))

s.listen(300)

listofbots = list()

while True:
	(clientsocket,address) = s.accept()
	print(address + ' is connected')
	t = threading.Thread(target=connectbot)
	listofbots.append(t)
	t.start()

for index in listofbots:
	index.join()

