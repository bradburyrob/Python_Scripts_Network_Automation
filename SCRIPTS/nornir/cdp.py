from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from rich import print
import os
import requests
import json
nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input("Enter Password: ")

def auto_config(task):
    neighbors = task.run(netmiko_send_command, command_string="sh cdp neigh", use_textfsm=True)
    task.host["facts"] = neighbors.result
    indexer = task.host["facts"]
    for index in indexer:
        local_int = index['local_interface']
        remoteInt = index['neighbor_interface']
        remoteDev = index['neighbor']
        remotePla = index['platform']
        newRemoteInt = remoteInt[0] + remoteInt.split(' ')[1]
        if "SEP" in remoteDev:

           x =1

        elif "AIR" in remotePla:

            print(task.host.hostname + " to WAP "  + remoteDev.split('.')[0]  + " " + newRemoteInt)

            task.run(netmiko_send_config, config_commands=["interface " + local_int,
                                                            "desc " + remoteDev.split('.')[0] + " " ,
                                                            "do wr"])

        else:
            print(task.host.hostname + " " +local_int + " to " + remoteDev.split('.')[0] + " "  + newRemoteInt)

            task.run(netmiko_send_config, config_commands=["interface " + local_int,
                                                       "desc " + remoteDev.split('.')[0]+ " " + newRemoteInt,
                                                       "do wr"])

results = nr.run(task=auto_config)
#import ipdb
#ipdb.set_trace()all-swi


'''
x =1
for my_arp in my_arps:

    if  ".10"  in  my_arp['interface'] and "101" not in my_arp['interface']:

        gold = my_arp['ip']
        print(gold, x)

        f = open("hosts2.yaml", "a")
        arpList = ("\n" +
                   str(x) +  "a:" + "\n"
                   "     hostname: " +     gold + "\n")
        f.writelines(arpList)
        x += 1
        f.close()
'''
