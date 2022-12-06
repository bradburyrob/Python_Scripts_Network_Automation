
from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
import datetime
nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):
    dateNow = datetime.date.today()
    writeToFile = open("VTP_STATUS_" + str(dateNow) + "_.csv","a")

    task.host["inventory"] = task.run(netmiko_send_command, command_string="sh vtp status | inc VTP Operating Mode ", use_textfsm=True).result

    inventory_items = task.host["inventory"]

    for item in inventory_items:
        VTP_MODE = item["mode"]
        VTP_DOMAIN = item["domain"]

        print(task.host.hostname,VTP_MODE , VTP_DOMAIN )
        writeToFile.writelines(task.host.hostname  +"," + VTP_MODE + "," + VTP_DOMAIN + "\n")

    writeToFile.close()

results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
