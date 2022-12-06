#!/usr/nin/env python
import paramiko, sys, time, hickle, os
from ciscoconfparse import CiscoConfParse
from datetime import date

hostnames = open('few-routers.txt').read().split()
username = input('Enter your Username:')
password = input('Enter your password:')
# username = ""
# password = "*"
now = date.today()
show_command = ('temp.txt')
Conditional_Config = ('conditional.txt')
# -----------------------------------------------
with open(show_command) as f:
    show = f.read()
# -----------------------------------------------
with open(Conditional_Config) as p:
    config = p.read()
# -----------------------------------------------
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for hostname in hostnames:
    response = os.system("ping  -n 1 " + hostname)

    if response == 0:
        ssh_client.connect(hostname=hostname, username=username, password=password)
        print("Succesful Connection", hostname)
        remote_connection = ssh_client.invoke_shell()
        remote_connection.send(show)
        time.sleep(16)
        output = remote_connection.recv(650000)
        config = str(output.decode()).splitlines()
        cisco_conf = CiscoConfParse(list(config))
        locations = cisco_conf.find_objects(r"^snmp-server locatio")
        for location in locations:

            place = print(str(hostname) + ' ' + str(location))
            reachable = os.system("echo Logged into router " + hostname  + " " + place + " >> C:\\Users\\Desktop\\EIGRP-log.txt" )
            #print(output.decode())
            time.sleep(4)

    else:
        print(hostname + " is offline")
        # print(output.decode())
        ssh_client.close
