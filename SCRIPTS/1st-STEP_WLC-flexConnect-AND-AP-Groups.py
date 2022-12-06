#!/usr/nin/env python
import paramiko, sys, time, hickle, os

hostname = input('Enter the WLC name or IP Address:')
username = input('Enter your Username:')
password = input('Enter your password:')
radius = input('Please Enter the Radius Server IP Address:')
key = input('Please input the radius key:')


groups = open('AP-fLexConnect-Sites.txt').read().split()
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
for group in groups:


	remote_connection.send("config wlan apgroup profile-mapping add " + group + "-APGRP1" + " Typical-Client-Density-802.11a" + "\n")
	time.sleep(3)
	remote_connection.send("y" + "\n")
	remote_connection.send("config wlan apgroup profile-mapping add " + group + "-APGRP1" + " Typical-Client-Density-802.11bg" + "\n")
	time.sleep(3)
	remote_connection.send("y" + "\n")
	time.sleep(3)
	remote_connection.send("config wlan apgroup interface-mapping add " + group + "-APGRP1" + " 1 usace_v502 " + "\n")
	time.sleep(3)
	remote_connection.send("config wlan apgroup interface-mapping add " + group + "-APGRP1" + " 2 management "  + "\n")
	time.sleep(3)
	remote_connection.send("config flexconnect group " + group + "-FLXGRP1" + " add" + "\n")
	time.sleep(3)
	remote_connection.send("config flexconnect group " + group + "-FLXGRP1" + " vlan enable" + "\n")
	time.sleep(3)
	remote_connection.send("config flexconnect group " + group + "-FLXGRP1" + " vlan native 501" + "\n")
	time.sleep(3)
	remote_connection.send("config flexconnect group " + group + "-FLXGRP1" + " wlan-vlan wlan 1 add vlan 502" + "\n")
	time.sleep(3)
	remote_connection.send("config flexconnect group " + group + "-FLXGRP1" + " radius server auth add primary " + radius + " 1812 "  + key + "\n")
	time.sleep(3)
	remote_connection.send("config flexconnect group " + group + "-FLXGRP1" + " radius server auth add secondary " + radius + " 1813 "  + key + "\n")
	time.sleep(3)
	remote_connection.send("config flexconnect group " + group + "-FLXGRP1" + " add" + "\n")
	time.sleep(3)
	remote_connection.send('\n')
	output = remote_connection.recv(650000)
	print(output.decode())


