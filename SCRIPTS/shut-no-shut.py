#!/usr/nin/env python
import paramiko, sys, time, hickle, os
from ciscoconfparse import CiscoConfParse

hostnames = open('few-routers.txt').read().split()
username = input('Enter your Username:')
password = input('Enter your password:')
# username = ""
# password = "*"
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
        all_ints = cisco_conf.find_objects(r"^interface")
        for int in all_ints:
            if int.re_search_children("NAC"):
                for line in int.ioscfg:
                    if "interface" in line:
                        print(line + " Removing NAC from the Interface")
                        remote_connection.send('\n')
                        remote_connection.send("config t\n")
                        #remote_connection.send("exit  " + '\n')
                        time.sleep(4)
                        remote_connection.send(line + '\n')
                        #remote_connection.send("description *** To C-SAJ-WAP-01 *** " + '\n')
                        time.sleep(3)
                        remote_connection.send('no mac access-group NAC_ACL in\n')
                        time.sleep(3)
                        remote_connection.send('\n')
                        remote_connection.send('end\n')
                        remote_connection.send('wr\n')
                        remote_connection.send('\n')
                        # print(output.decode())
                        time.sleep(4)

    else:
        print(hostname + " is offline")
        # print(output.decode())
        ssh_client.close
