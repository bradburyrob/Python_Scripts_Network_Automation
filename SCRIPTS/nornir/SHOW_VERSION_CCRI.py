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
    writeToFile = open("Show_Version" + str(dateNow) + "_Query.csv","a")
    try:
        task.host["inventory"] = task.run(netmiko_send_command, command_string="show version", use_textfsm=True).result

        Devices = task.host["inventory"]
        for Device in Devices:
            version = str(Device['version'])
            image   = str(Device['running_image'])
            model   = str(Device['hardware'])
            print(task.host.hostname,model,version,image)
            Status = (task.host.hostname+ "," +version + "," + model + ","+ image + "\n")
            writeToFile.writelines(Status)



    except:
        print(task.host.hostname + " TIMEOUT")
        writeToFile.writelines(task.host.hostname + " ,TIMEOUT"  + "\n")

    writeToFile.close()
    task.run(netmiko_send_command, command_string="exit")

results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
