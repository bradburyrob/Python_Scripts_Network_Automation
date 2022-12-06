from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):

    try:
        task.run(netmiko_send_command, command_string="sh interface lo0" )
        task.host["inventory"] = task.run(netmiko_send_command, command_string="sh interface lo0", use_textfsm=True).result
        LoopBacks = task.host["inventory"]

        for lo0 in LoopBacks:
            ipAddress = lo0["ip_address"]

            print(task.host.hostname,   ipAddress)


            f = open("Lo0_Check.v2.txt", "a")
            tunnalStatus1 = (task.host.hostname + " | "+   ipAddress  + "\n")
            f.writelines(tunnalStatus1)
            f.close()

    except:
        print(task.host.hostname + " failed to connect or pull data")
        f = open("Lo0_Check.v2.txt", "a")
        tunnalStatus3 = (task.host.hostname + " did not connect to router" + "\n")
        f.writelines(tunnalStatus3)
        f.close()


results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
