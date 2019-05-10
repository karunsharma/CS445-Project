# CS 445 Final Project

## Author
## Karun Sharma

## About
This a final project for the class CS445 at the University of Nevada, Reno in which this project is similar to the Mirai Botnet, it utilizes python, socket programming, and threading to perform certain attacks such as SYN flood, flooding using plain packets that are of random byte size, and installing malicious content on a target VM. All attacks are performed on Kali Linux machines using a host-only adapter

## What I've learned
The Mirai Botnet is a botnet in which an attacker has a CNC (Command and Control server) set up and will asynchrousnly scan and try and SSH into IoT devices using a bruteforce technique. Once the Iot Device is accessed, the CNC can send commands to these devices which execute these attacks on a target server. This project achieves this goal by following a similar architecture and providing popular attack methods where the CNC.py script will be the server and the Attacker.py script will scan for IP addresses within a certain bound and install the ConnecttoCNC.py script on these IoT VM's through SSH and run this script which will use socket programming to connect back to the CNC and the CNC will now send commands of attack through TCP packets and will use the IoT VM's will use Scapy to execute these attacks.

# How to run

### Attacker VM
```
python CNC.py
python Attacker.py
```

## To Quit
Pressing 5 in the CNC program will terminate connections bewteen server and clients, but to close out the server, you will need to manually close the CNC.py terminal window

### Regarding Commits
If you see commits by the name "Root" that is me Karun Sharma, I had issues configuring my git username and email on my local machine

### Important Notes
Please have a ssh service set up for both Iot VM's and Server VM
Root also needs to be enabled on the ssh configuration which can done by opening this file in terminal
```
nano /etc/ssh/sshd_config
```
Then making sure PermitRootLogin is set to yes and the "#" is also removed on that line

Then you can start the SSH service
```
service ssh start
```
## Please start SSH before running the programs

### Config File (Config.txt)
There is a Config.txt file which is very important in which you can replace the ip addresses of the various fields to match your VM

TARGET_SERVER = The IP address of the VM that will be attacked
HOST_SERVER = The IP address of the attacker VM

```
RANGE_OF_IP = The IP range in which you want searched

For example the ip addreeses of my VM's all started with 192.168.56.
```

### Nmap Python Library
This repo also has a folder called nmap, please place this folder in your root directory as well for the IoT VM's. This folder was downloaded from http://xael.org/pages/python-nmap-en.html

I had issues in which using pip install python-nmap wasn't working for me, so I had to resort to downloading the source folder and manually placing it in proper directories

### Password File (Passwords.txt)
This file is used to SSH into the IoT machines VM. I only had select passwords in here to simplicity, feel free to add more if needed

### Content File (content.txt)
This file is the file that is considered the malicious content and is used when executing a install a malicious content attack. This file is opened in a endless loop using the ComputerCrash.py script

### SSHPasswords (SSHPasswords.txt)
This file is the file that is used for when trying to SSH into a server to install the malicious content. Every bot is allocated a certain amount of passwords and they utilze them to SSH into the machine

## Important Dependencies
```
- nmap
- paramiko
- scapy
- socket

```
## Monitoring Attacks
SYN flood and flooding using random byte packets can be monitored using Wireshark on the target VM
