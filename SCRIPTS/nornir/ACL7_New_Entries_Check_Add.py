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
    writeToFile = open("ACL7_Status.csv","a")
    Router_Name = task.host.hostname
    try:

        task.host["Interface_Query1"] = task.run(netmiko_send_command, command_string="sh access-lists 7 | i 10.194.0.112").result
        task.host["Interface_Query2"] = task.run(netmiko_send_command, command_string="sh access-lists 7 | i 10.196.0.112").result

        if "10.194.0.112" in str(task.host["Interface_Query1"]) and  "10.196.0.112" in str(task.host["Interface_Query2"]) :
            ACL7_Entry1 = str(task.host["Interface_Query1"]).split()[2]
            ACL7_Entry2 = str(task.host["Interface_Query2"]).split()[2]
        else:
            ACL7_Entry1 = " IP 1 not configured"
            ACL7_Entry2 = " IP 2 not configured"

        print(Router_Name + " ACL7 has the following  " + " " + " " + ACL7_Entry1 + " " + ACL7_Entry2)
        writeToFile.writelines(Router_Name + "," + ACL7_Entry1 + "," + ACL7_Entry2 + "," + str(dateNow) + "\n")


    except Exception as E:
        print(Router_Name + " error connecting " + str(E))
        writeToFile.writelines(Router_Name + "," + " " + "," + str(E) + "," + str(dateNow) + "\n")

results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
