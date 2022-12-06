from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):

    try:
        task.run(netmiko_send_command, command_string="sh start | sec crypto ipsec profile DMVPN" )
        task.host["inventory"] = task.run(netmiko_send_command, command_string="sh start | sec crypto ipsec profile DMVPN", use_textfsm=True).result
        tunnels = task.host["inventory"]
        if "group2" in tunnels:

            print( task.host.hostname + " has DH 2 configured, needs to be corrected")
        else:
            print( task.host.hostname + " has DH 14 configured")

    except:
        print(task.host.hostname + " failed to connect or pull data")


results = nr.run(task=auto_config)

print_result(results)


#import ipdb
#ipdb.set_trace()
