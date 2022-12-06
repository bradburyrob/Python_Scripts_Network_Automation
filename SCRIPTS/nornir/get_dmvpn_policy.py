from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from ciscoconfparse import CiscoConfParse
import json


nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password =input("Enter Password ")

def auto_config(task):

    try:
        tunnel10 = task.run(netmiko_send_command, command_string="show interface tunnel 10" ).result
        tunnel20 = task.run(netmiko_send_command, command_string="show interface tunnel 20" ).result

        if "DMVPN-Profile-1" in tunnel10:
            print(task.host.hostname + " Tunnel 10 has DMVPN-Profile-1")
            f = open("tunnelStatus.v3.txt", "a")
            tunnalStatus1 = (task.host.hostname + " Tunnel 10 has DMVPN-Profile-1" + "\n")
            f.writelines(tunnalStatus1)
            f.close()
        else:
            print(task.host.hostname + " WRONG POLICY in Tunnel 10")
            f = open("tunnelStatus.v3.txt", "a")
            tunnalStatus1 = (task.host.hostname + " WRONG POLICY in Tunnel 10" + "\n")
            f.writelines(tunnalStatus1)
            f.close()

        if "DMVPN-Profile-2" in tunnel20:
            task.host.hostname + " Tunnel 20 has DMVPN-Profile-2"
            f = open("tunnelStatus.v3.txt", "a")
            tunnalStatus2 = (task.host.hostname + " Tunnel 20 has DMVPN-Profile-2" + "\n")
            f.writelines(tunnalStatus2)
            f.close()
        else:
            print(task.host.hostname + " WRONG POLICY in Tunnel 20")
            f = open("tunnelStatus.v3.txt", "a")
            tunnalStatus2 = (task.host.hostname + " WRONG POLICY in Tunnel 20" + "\n")
            f.writelines(tunnalStatus2)
            f.close()

    except:
        print("Was not able to parse output")
        tunnalStatus3 = (task.host.hostname + " did not connect to router" + "\n")
        f.writelines(tunnalStatus3)
        f.close()


results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
