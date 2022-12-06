from nornir import InitNornir
from nornir_netmiko import *
from nornir_utils.plugins.functions import print_result
import json

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input("Enter password: ")

def auto_config(task):
   router_arps =task.run(netmiko_send_command, command_string="show ip int brief  | e una", use_textfsm=True)
   task.host["facts"] = router_arps.result

   arp_results = task.host["facts"]
   for arp_result in arp_results:
      if arp_result["intf"] == "Vlan10":
         print(arp_result["intf"]  + " " + arp_result["ipaddr"])
         task.run(netmiko_send_config, config_commands=["interface " + "vlan 10" ,
                                               "desc   *** MGMT ***",
                                               "ip address " + arp_result["ipaddr"] +  " 255.255.255.192",
                                               "do wr"])



results = nr.run(task=auto_config)


#import ipdb
#ipdb.set_trace()


