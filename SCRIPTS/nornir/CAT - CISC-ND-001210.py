from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):

    try:
        task.run(netmiko_send_command, command_string="sh run | s ^ip ssh server algorithm encryption" )
        task.host["inventory"] = task.run(netmiko_send_command, command_string="sh run | s ^ip ssh server algorithm encryption", use_textfsm=True).result
        crypto = task.host["inventory"]
        if "ip ssh server algorithm encryption aes256-ctr aes192-ctr aes128-ctr" in crypto:

            print( task.host.hostname + " CAT I CISC-ND-001210 Compliant")
        else:
            print( task.host.hostname + " missing cryptographic mechanisms to protect the confidentiality of remote maintenance session")

    except:
        print(task.host.hostname + " failed to connect or pull data")


results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
