#!/usr/nin/env python
import paramiko, sys, time, hickle, os
from ciscoconfparse import CiscoConfParse

hostnames = open('few-routers.txt').read().split()
username = input('Enter your Username:')
password = input('Enter your password:')
# username = ""
# password = "*"
show_command = ('show_ver.txt')
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

        if("2102" in output.decode()):
            print(str(hostname) + ' Router ' )
            reachable = os.system("echo Logged into router " + hostname +  " this is a Router" ">> C:\\Users\\Desktop\\NTP-2-log.txt" )
            #print(output.decode())
            time.sleep(4)
        elif("0x102" in output.decode()):
            print(str(hostname) + ' Switch')
            reachable = os.system("echo Logged into router " + hostname + " this is likely a switch" ">> C:\\Users\\Desktop\\NTP-2-log.txt")
            # print(output.decode())
            time.sleep(4)

        else:
            print(str(hostname) + ' CONFREG has been altered for password recovery')
            reachable = os.system("echo Logged into router " + hostname + " CONFREG has been altered for password recovery" ">> C:\\Users\\Desktop\\NTP-2-log.txt")
            # print(output.decode())
            time.sleep(4)
    else:
        print(hostname + " is offline")
        # print(output.decode())
        ssh_client.close
