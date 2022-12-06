#!/usr/nin/env python
import paramiko, sys, time, hickle, os
from ciscoconfparse import CiscoConfParse

hostnames = open('ew-routers.txt').read().split()
username = input('Enter your Username:')
password = input('Enter your password:')
# username = ""
# password = "*"
show_command = ('show_ntp_status.txt')
Conditional_Config = ('ntp.txt')
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
            remote_connection.send(show)
            time.sleep(16)
            output = remote_connection.recv(650000)
            if("Clock is synchronized" in output.decode()):
                reachable = os.system("echo Logged into router " + hostname +  " Clock is synchronized" + " >> C:\\Users\\Desktop\\NTP-log.txt" )

                print("echo Logged into router " + hostname +  " Clock is synchronized")
                #remote_connection.send('\n')
                #remote_connection.send(config)
                #remote_connection.send('\n')
                #rint(output.decode())
                #time.sleep(4)
            else:
                reachable = os.system("echo Logged into router " + hostname +  " Clock is NOT synchronized" + " >> C:\\Users\\Desktop\\NTP-log.txt" )

                print("echo Logged into router " + hostname +  " Clock is NOT synchronized")
                #rint(output.decode())
                #remote_connection.send('\n')

        except:
            unreachable = os.system("echo  This router does not have TACACS enabled : router " + hostname +  " >> C:\\Users\\Desktop\\NTP-log.txt" )
            print(unreachable)

    else:
        offiline = os.system("echo  This router is OFFLINE, not pinging " + hostname + " >> C:\\Users\\Desktop\\NTP-log.txt")
        print(offiline)
       # print(output.decode())
ssh_client.close
