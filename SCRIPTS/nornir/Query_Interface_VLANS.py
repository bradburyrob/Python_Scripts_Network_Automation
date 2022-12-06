
from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
nr = InitNornir("config2.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):


    task.host["inventory"] = task.run(netmiko_send_command, command_string="show ip interface brief | in Vlan20", use_textfsm=True).result

    inventory_items = task.host["inventory"]

    for item in inventory_items:
        vlan = item["intf"]
        vlan_status = item["status"]

   #

        print(task.host.hostname, vlan, vlan_status )


results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
