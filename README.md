# CS445 Final Project

## About
This a final project for the class CS445 at the University of Nevada, Reno in which this project is similar to the Mirai Botnet, it utilizes python, socket programming, and threading to perform certain attacks such as SYN flood, flooding using plain packets, and installing malicious content on a target VM. All attacks are performed on Kali Linux machines using a host-only adapter

## How to run

### Attacker VM
```
python CNC.py
python Attacker.py
```

## Regarding Commits
If you see commits by the name "Root" that is me Karun Sharma, I had issues configuring my git username and email on my local machine

### Important Notes
Please have a ssh service set up for both Iot VM's and Server VM
Root also needs to be enabled on the ssh which can done by opening the file in terminal
```
nano /etc/ssh/sshd_config
```
Then making sure PermitRootLogin is to yes and the "#" is also removed on that line

Then you can start the SSH service
```
service ssh start
```


### Config File (Config.txt)
There is a Config.txt file which is very important in which you can replace the ip addresses of the various fields to match your VM

TARGET_SERVER = <The IP address of the VM that will be attacked>
HOST_SERVER = <The IP address of the attacker VM>
```
RANGE_OF_IP = <The IP range in which you want searched>

For example the ip addreeses of my VM's all started with 192.168.56.
```

### Nmap Python Library
This repo also has a folder called nmap, please place this folder in your root directory as well for the IoT VM's

### Password File (Passwords.txt)
This file is used to SSH into the IoT machines VM. I only had select passwords in here to simplicity, feel free to add more if needed

### Content File (content.txt)
This file is the file that is considered the malicious content and is used when executing a install a malicious content attack. This file is opened in a endless loop using the ComputerCrash.py script

### SSHPasswords (SSHPasswords.txt)
This file is the file that is used for when SSH into a server to install the malicious content. Every bot is allocated a certain amount of passwords and they utilze them to SSH into the machine

## Issues in the project
The only issue i've found is that the flooding using random packets does not work when using the option of finding Iot devices within a range from the config file. So to run that option, when running python Attacker.py, I would run the ConnecttoCNC.py script manually on the Iot VM's and then call the flooding using plain packets option from the CNC.py 

So this is how the commands would look if using the flooding using random sized plain packets option

### Attacker VM
```
python CNC.py
```

### IoT VM
```
python ConnecttoCNC.py
```

### Attacker VM
Select the option to flood using plain packets