from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
import datetime


nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password =  input("Enter Password: ")

def auto_config(task):
    dateNow = datetime.date.today()
    writeToFile = open("DHCP_Snooping_Status.csv","a")
    Router_Name = task.host.hostname
    try:

        task.host["Snooping_Query"] = task.run(netmiko_send_command, command_string="show ip dhcp snooping | i Switch DHCP snooping is").result
        Snooping_State = str(task.host["Snooping_Query"]).split()[4]

        task.host["Interface_Query"] = task.run(netmiko_send_command, command_string="show ip dhcp snooping | i net").result
        Snooping_Interface = ""
        if task.host["Interface_Query"]:
            Snooping_Interface = str(task.host["Interface_Query"]).split()[0]
        else:
            Snooping_Interface = " empty"

        print(Router_Name + " DHCP Snooping is " + Snooping_State + " " + Snooping_Interface)
        writeToFile.writelines(Router_Name + "," + Snooping_State + "," + Snooping_Interface + "," + str(dateNow) + "\n")


    except Exception as E:
        print(Router_Name + " error connecting " + str(E))
        writeToFile.writelines(Router_Name + "," + " " + "," + str(E) + "," + str(dateNow) + "\n")

results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
