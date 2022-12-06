from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
import datetime

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input("Enter Password: ")

def auto_config(task):
    dateNow = datetime.date.today()
    writeToFile = open( "EIGRP_Key_25_Update-"+ str(dateNow) +".csv", "a")

    try:
        task.host["inventory1"] = task.run(netmiko_send_command, command_string="show ip protocols | i Routing Protocol is").result
        EIGRP = task.host["inventory1"]
        if  "eigrp"  in EIGRP:

            task.host["inventory"] = task.run(netmiko_send_command, command_string="show key chain EIGRP").result
            EIGRP_Key_25 = task.host["inventory"]
            if  "send lifetime (12:00:00 UTC Jun 16 2022) - (12:00:00 UTC Dec 14 2023)"  in EIGRP_Key_25:

                print( task.host.hostname + " , Key 25 needs to be updated" )
                writeToFile.writelines(task.host.hostname + " ,Key 25  is WRONG, send lifetime (12:00:00 UTC Jun 16 2022) - (12:00:00 UTC Dec 14 2023)," + str(dateNow) + "\n")
                task.run(netmiko_send_config, config_file="C:\\Users\\r1acer1b\\Desktop\\CONFIGS\\FIX.txt")

            else:
                print( task.host.hostname + "  ,Key 25 is correct 25 is OK ")
                writeToFile.writelines(task.host.hostname + " ,Key 25  is CORRECT, send lifetime (12:00:00 UTC Jun 16 2023) - (12:00:00 UTC Dec 14 2023)," + str(dateNow) + "\n")
        else:
            print(task.host.hostname + "  , Not running EIGRP ")
            writeToFile.writelines(task.host.hostname  + "," + "Not Running EIGRP" +"," + "," + str(dateNow) + "\n")

    except Exception as E:
        print(task.host.hostname + " TIMEOUT     " + str(E))
        writeToFile.writelines(task.host.hostname + " ,TIMEOUT "  +  str(E) + "," +  str(dateNow) + "\n")

    writeToFile.close()


results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
