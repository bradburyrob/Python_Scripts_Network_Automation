#!/usr/nin/env python
import paramiko, sys, time, hickle, os
from ciscoconfparse import CiscoConfParse

hostnames = open('\few-routers.txt').read().split()
username = input('Enter your Username:')
password = input('Enter your password:')
# username = ""
# password = "*"
show_command = ('\\Desktop\\Python\\temp.txt')
Conditional_Config = ('\\Python\\conditional.txt')
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
        try:
            ssh_client.connect(hostname=hostname, username=username, password=password)
            print("Succesful Connection", hostname)
            remote_connection = ssh_client.invoke_shell()
            output = remote_connection.recv(650000)
            reachable = os.system("echo Logged into router " + hostname +  " >> Desktop\\EIGRP-log.txt" )

            print(reachable)
            remote_connection.send('\n')
            remote_connection.send(config)
            remote_connection.send('\n')
            # print(output.decode())
            time.sleep(4)

        except:
            unreachable = os.system("echo  This router does not have TACACS enabled : router " + hostname +  " >> EIGRP-log.txt" )
            print(unreachable)

    else:
        offiline = os.system("echo  This router is OFFLINE, not pinging " + hostname + " >> IGRP-log.txt")
        print(offiline)
       # print(output.decode())
ssh_client.close
