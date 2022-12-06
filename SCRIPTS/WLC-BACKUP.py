#!/usr/nin/env python
import paramiko, sys, time, hickle, os
from datetime import date

username = ""
password = ""
now = date.today()

WLCs = open('Wireless-Controllers.txt').read().split()
#-----------------------------------------------

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for WLC in WLCs:

	ssh_client.connect(hostname=WLC,username=username,password=password)
	print ("Succesful Connection", WLC)
	remote_connection = ssh_client.invoke_shell()
	output = remote_connection.recv(650000)
	time.sleep(3)
	remote_connection.send(username + '\n')
	time.sleep(3)
	remote_connection.send(password + '\n')
	time.sleep(3)
#------------------------------------------------
	if WLC == "10.8.10.244":
		WLC = "CPCW01"
		remote_connection.send("transfer upload mode ftp  \n")
		time.sleep(3)
		remote_connection.send("transfer upload datatype config  \n")
		time.sleep(3)
		remote_connection.send("transfer upload filename "  + WLC  + "-" + str(now)  + "-BCKUP"  "\n")
		time.sleep(3)
		remote_connection.send("transfer upload username ftp-user \n")
		time.sleep(3)
		remote_connection.send("transfer upload  password t3amw0rk \n")
		time.sleep(3)
		remote_connection.send("transfer upload path /CPI-BACKUPS  \n")
		time.sleep(3)
		remote_connection.send("transfer upload serverip z.z.z.z  \n")
		time.sleep(3)
		remote_connection.send("transfer upload start  \n")
		time.sleep(3)
		remote_connection.send("y" + "\n")
		time.sleep(40)




	else:
		remote_connection.send("transfer upload mode ftp  \n")
		time.sleep(3)
		remote_connection.send("transfer upload datatype config  \n")
		time.sleep(3)
		remote_connection.send("transfer upload filename " + WLC + "-" + str(now) + "-BCKUP"  "\n")
		time.sleep(3)
		remote_connection.send("transfer upload username ftp-user \n")
		time.sleep(3)
		remote_connection.send("transfer upload  password t3amw0rk \n")
		time.sleep(3)
		remote_connection.send("transfer upload path /CPI-BACKUPS  \n")
		time.sleep(3)
		remote_connection.send("transfer upload serverip x.x.x.x  \n")
		time.sleep(3)
		remote_connection.send("transfer upload start  \n")
		time.sleep(3)
		remote_connection.send("y" + "\n")
		time.sleep(40)


	print(WLC,now)


	output = remote_connection.recv(650000)
	print(output.decode())


