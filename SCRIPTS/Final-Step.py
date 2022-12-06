#!/usr/nin/env python
import paramiko, sys, time, hickle, os

hostname = input('Enter the WLC name or IP Address:')
username = input('Enter your Username:')
password = input('Enter your password:')
group = input('Please Enter the Group name:')



APS = open('C:\\Users\\r1acer1b\\Desktop\\Python\\few-waps.txt').read().split()
#-----------------------------------------------

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


ssh_client.connect(hostname=hostname,username='null',password='null')
print ("Succesful Connection", hostname)
remote_connection = ssh_client.invoke_shell()
output = remote_connection.recv(650000)
time.sleep(3)
remote_connection.send(username + '\n')
time.sleep(3)
remote_connection.send(password + '\n')
time.sleep(3)
for AP in APS:


	remote_connection.send("config  ap mode flexconnect submode wips " + AP +  "\n")
	time.sleep(3)
	remote_connection.send("y" + "\n")
	remote_connection.send("config ap group-name " + group + "-APGRP1 " + AP + "\n")
	time.sleep(3)
	remote_connection.send("y" + "\n")
	time.sleep(3)
	remote_connection.send('\n')
	output = remote_connection.recv(650000)
	print(output.decode())


