'''
File: Attacker.py
Description: This script will try to guess the IP addreses of the target machine and send them the zombie VM's
Author: Karun Sharma
Date: 4-14-19
'''

import random

def generateipaddresses():
	tupleofipaddresses = list()
	for index in range(10):
		tupleofipaddresses.append('.'.join(str(random.randint(0,255)) for inner in range(4)))

	return tupleofipaddresses

result = 0

zombiesvms = raw_input("Enter the number of Zombie VM's: ")
referencetozombievms = list()
for index in range(int(zombiesvms)):
	ipaddresses = raw_input("Enter the ip addresses of Zombie VM {}: ".format(index + 1))
	referencetozombievms.append(ipaddresses)

print(referencetozombievms)

while int(result) != 3:
	print("Choose from the following commands below")
	print("1) Generate random IP addresses\n 2) Send IP addresses to zombie VM's\n 3)Exit")
	result = raw_input("Enter a number: ")

	if int(result) == 1:
		ipaddresses = generateipaddresses()
		print(ipaddresses)

