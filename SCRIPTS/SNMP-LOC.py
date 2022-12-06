#!/usr/nin/env python
import  csv
import paramiko, sys, time, hickle, os

username = input('Enter your Username:')
password = input('Enter your password:')
#-----------------------------------------------

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


with open('nwwdwo-SNMP-Loc.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            hostname = row[0]
            response = os.system("ping  -n 1 " + hostname)
            if response == 0:
                ssh_client.connect(hostname=hostname, username=username, password=password)
                print("Succesful Connection", hostname)
                remote_connection = ssh_client.invoke_shell()
                remote_connection.send("config t\n")
                remote_connection.send('snmp-server location ' + row[1] +'\n')
                remote_connection.send(' end  \n  ')
                remote_connection.send('wr\n')
                remote_connection.send('\n')

                print(f'\t{row[0]}   {row[1]}')

            line_count += 1
        else:
            print("not line 0")
            line_count += 1
    print(f'Processed {line_count} lines.')