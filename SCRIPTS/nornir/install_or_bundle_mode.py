from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):

    try:
        task.run(netmiko_send_command, command_string="show ver" )
        task.host["inventory"] = task.run(netmiko_send_command, command_string="show ver").result
        installMode = task.host["inventory"]
        if  "INSTALL"  in installMode:

            print( task.host.hostname + " ,Switch in INSTALL mode" )



        else:

            print( task.host.hostname + "  ,switch is in BUNDLE ")


    except:
        print(task.host.hostname + " failed to connect or pull data")


results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
