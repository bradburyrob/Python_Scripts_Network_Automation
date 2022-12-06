from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
import os, datetime,rich

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):
    dateNow = datetime.date.today()
    writeToFile = open("COPP_STATUS_IOS_AND_XE_" + str(dateNow) + "_Query.csv","a")
    try:
        task.host["inventory"] = task.run(netmiko_send_command, command_string="show policy-map control-plane  | i Service-policy input:", use_textfsm=True).result
        policies = task.host["inventory"]
        if policies != "":
            writeToFile.writelines(task.host.hostname + "," +  policies + "\n")
            print(task.host.hostname, policies )
        else:
            writeToFile.writelines(task.host.hostname + "," + "NO COPP Applied" + "\n" )
            print(task.host.hostname +"," + " NO COPP  applied" )

    except:
        print(task.host.hostname + " TIMEOUT")
        writeToFile.writelines(task.host.hostname + " ,TIMEOUT"  + "\n")

    writeToFile.close()
    task.run(netmiko_send_command, command_string="exit")

results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
