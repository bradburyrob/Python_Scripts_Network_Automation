from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):

    try:
        task.run(netmiko_send_command, command_string="sh interface status | include 501" )
        task.host["inventory"] = task.run(netmiko_send_command, command_string="sh interface status | include 501").result
        WAP_Interface = str(task.host["inventory"]).split(sep=" ")

        if "501" in WAP_Interface:
            print( task.host.hostname + "  ", WAP_Interface)

            '''task.run(netmiko_send_config, config_commands=["default interface " + WAP_Interface[0],
                                                           "interface " + WAP_Interface[0],
                                                           "description *** WAP-01   ***",
                                                           "switchport trunk encapsulation dot1q",
                                                           "switchport trunk native vlan 501",
                                                           "switchport trunk allowed vlan 501,502",
                                                           "switchport mode trunk",
                                                           "switchport nonegotiate",
                                                           "do wr"])'''

        else:
            print( task.host.hostname + " no access ports with vlan 501 ")


    except:
        print(task.host.hostname + " failed to connect or pull data")


results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
