from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from rich import print
import os, datetime
import requests
import json

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = ""

def auto_config(task):
    interface = ""
    outgoing_acl = ""
    inbound_acl = ""
    ipaddr = ""
    LOCAL_ROUTER_SWITCH_ADDRESSES_Group = ""
    dateNow = datetime.date.today()
    writeToFile = open("Internal_ACL_Deployment.csv","a")
    router = task.host.hostname
    try:
        CSM_STATE = task.run(netmiko_send_command, command_string="sh ip interface | include CSM").result
        Interfaces = task.run(netmiko_send_command, command_string="sh ip interface", use_textfsm=True)
        task.host["Interfaces"] = Interfaces.result
        indexer = task.host["Interfaces"]

        if "CSM" in CSM_STATE:
            print(router + " is managed by CSM")
            writeToFile.writelines(router + "," + "" + "," + " is managed by CSM " + "," + str(dateNow) + "\n")
        else:
             #task.run(netmiko_send_config,config_file="\\OBJECT_GROUPS.txt")
             #task.run(netmiko_send_config, config_file="\\INTERNAL_ACL.txt")
             for index in indexer:
                 interface      = index['intf']
                 outgoing_acl   = index['outgoing_acl']
                 inbound_acl    = index['inbound_acl']
                 ipaddr         = index['ipaddr']
                 mask           = index['mask']

                 if ipaddr:
                     print(router + " NO CSM "  + interface + " " + outgoing_acl + " " + inbound_acl + " " + str(ipaddr) + " " + str(mask) )
                     for i in ipaddr:
                         print( " host " + i )
                         #task.run(netmiko_send_config, config_commands=["object-group network LOCAL_ROUTER_SWITCH_ADDRESSES", "host " + i, ""])
                         if inbound_acl or outgoing_acl:
                             print("An ACL is already applied " + inbound_acl + outgoing_acl)
                             #writeToFile.writelines(router + "," + interface + "," + inbound_acl + "," + str(dateNow) + "\n")
                         else:
                             print("No ACL applied")
                             #task.run(netmiko_send_config, config_commands=["interface " + interface,"ip access-group PROTECT_RTR_SW_ACL in",""])
                             #writeToFile.writelines(router + "," + interface + "," + "PROTECT_RTR_SW_ACL in" + "," + str(dateNow) + "\n")

    except Exception as E:
        print(router + " error connecting " + str(E))
        writeToFile.writelines(router + "," + " " + "," + str(E) + "," + str(dateNow) + "\n")

results = nr.run(task=auto_config)
#import ipdb
#ipdb.set_trace()


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

# print(router, "NEW ACL NOT APPLIED" , inbound_acl)
# print(router + " " +  interface + " " + outgoing_acl + " " + inbound_acl+ " " + ipaddr )
# task.run(netmiko_send_config, config_commands=["interface " + interface,
#                                               "no ip access-group PROTECT_ROUTERS_AND_SWITCHES in",
#                                               ""])
