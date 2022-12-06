#!/usr/nin/env python
import paramiko, sys, time, hickle, os
from ciscoconfparse import CiscoConfParse

hostnames = open('few-routers.txt').read().split()
username = "input('Enter your Username:')"
password = input('Enter your password:')
#username = ""
#password = "*"
show_command = ('temp.txt')
Conditional_Config = ('conditional.txt')
#-----------------------------------------------
with open(show_command) as f:
		show = f.read() 
#-----------------------------------------------
with open(Conditional_Config) as p:
		config = p.read()
#-----------------------------------------------
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


for hostname in hostnames:
	response = os.system("ping  -n 1 "  + hostname  )
	
	if response == 0:
		ssh_client.connect(hostname=hostname,username=username,password=password)
		print ("Succesful Connection", hostname)
		remote_connection = ssh_client.invoke_shell()
		remote_connection.send(show)
		time.sleep(30)
		output= remote_connection.recv(650000)
		config = str(output.decode()).splitlines()
		cisco_conf = CiscoConfParse(list(config))
		all_ints = cisco_conf.find_objects(r"^interface")
		for int in all_ints:
			if int.re_search_children("switchport access vlan 501"):
				for  line in int.ioscfg:
					if "interface" in line:
						print(line + " Just configuring the VLANS")
						remote_connection.send('\n')
						remote_connection.send("config t\n")
						remote_connection.send('vlan 502\n')
						remote_connection.send(' name WIFI_USACE_V502  \n  ')
						remote_connection.send('vlan 501\n')
						remote_connection.send('name WIFI_MGMT_V501\n')
						remote_connection.send('vlan 503\n')
						remote_connection.send('name WIFI_VOIP_V503\n')
						remote_connection.send("exit  " + '\n')
						remote_connection.send("default  " + line + '\n')
						time.sleep(10)
						remote_connection.send(line + '\n')
						time.sleep(10)
						remote_connection.send('description *** WAP ***\n')
						remote_connection.send('switchport trunk encapsulation dot1q\n')
						remote_connection.send('switchport trunk native vlan 501\n')
						remote_connection.send('switchport trunk allowed vlan 501,502\n')
						remote_connection.send('switchport mode trunk\n')
						remote_connection.send('switchport nonegotiate\n')
						remote_connection.send('end\n')
						remote_connection.send('wr\n')
						remote_connection.send('\n')
						#print(output.decode())
						time.sleep(4)

		else:
			print(hostname + " is offline")
		#print(output.decode())
		ssh_client.close
