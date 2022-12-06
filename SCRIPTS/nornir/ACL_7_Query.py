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
    writeToFile = open( "ACL7_Status-"+ str(dateNow) +".csv", "a")

    try:
        task.host["inventory"] = task.run(netmiko_send_command, command_string="show run all | in 10.194.0.112|10.196.0.112").result
        acl7 = task.host["inventory"]
        if  "10.194.0.112"  not in acl7:

            print( task.host.hostname + " , ACL needs to be updated" )
            writeToFile.writelines(task.host.hostname + " ,ACL needs to be updated,Violation" + "\n")
            task.run(netmiko_send_config, config_file="C:\\Users\\r1acer1b\\Desktop\\CONFIGS\\ACL7.txt")

        else:

            print( task.host.hostname + "  ,ACL 7 is OK ")
            writeToFile.writelines(task.host.hostname + " , ACL 7 is OK,Compliant" + "\n")


    except:
        print(task.host.hostname + " TIMEOUT")
        writeToFile.writelines(task.host.hostname + " ,TIMEOUT,TIMEOUT" + "\n")

    writeToFile.close()


results = nr.run(task=auto_config)

print_result(results)


#import ipdb
#ipdb.set_trace()
