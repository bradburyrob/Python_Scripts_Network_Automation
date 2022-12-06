#!/usr/nin/env python
import paramiko, sys, time, hickle, os
from ciscoconfparse import CiscoConfParse

hostnames = open('script-Routers.txt').read().split()
username = "input('Enter your Username:')"
password = input('Enter your password:')

show_command = ('show-command.txt')
Send_Config = ('conditional.txt')
# -----------------------------------------------
with open(show_command) as f:
    show = f.read()
# -----------------------------------------------
with open(Send_Config) as p:
    configs = p.read()
# -----------------------------------------------
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for hostname in hostnames:
    #response = os.system("ping  -n 1 " + hostname + "| echo off")
    try:

        ssh_client.connect(hostname=hostname, username=username, password=password)
        #print("Succesful Connection", hostname)
        remote_connection = ssh_client.invoke_shell()
        remote_connection.send(show)
        time.sleep(1)
        output = remote_connection.recv(650000)
        config = str(output.decode()).splitlines()
        cisco_conf = CiscoConfParse(list(config))
        usernames = cisco_conf.find_lines(linespec="aaa common-criteria policy", exactmatch=False)


        print(hostname + " Applying to  username")
        remote_connection.send(" configure terminal \n")
        remote_connection.send(" aaa common-criteria policy PASSWORD_POLICY\n")
        remote_connection.send(" min-length 15\n")
        remote_connection.send(" max-length 127\n")
        remote_connection.send(" numeric-count 1\n")
        remote_connection.send(" upper-case 1\n")
        remote_connection.send(" lower-case 1\n")
        remote_connection.send(" special-case 1\n")
        remote_connection.send(" char-changes 8\n")
        remote_connection.send(" exit\n")
        remote_connection.send(" no  enable secret\n")
        remote_connection.send("no username \n")
        remote_connection.send("Y\n")

        remote_connection.send(" exit\n")
        remote_connection.send(" end\n")
        time.sleep(10)



        #print(output.decode())
        ssh_client.close()

    except:
        print("Could not ssh to " + hostname)
