from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
import datetime

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):
    dateNow = datetime.date.today()
    writeToFile = open( "OSPF_Key_7_Update-"+ str(dateNow) +".csv", "a")

    try:
        task.host["inventory1"] = task.run(netmiko_send_command, command_string="show ip ospf").result
        OSPF = task.host["inventory1"]
        if  "Routing Process"  in OSPF:

            task.host["inventory"] = task.run(netmiko_send_command, command_string="sh key chain OSPF_KEY_CHAIN_1 ").result
            OSPF_Key_7 = task.host["inventory"]
            if  "send lifetime (12:00:00 UTC Jun 16 2023) - (12:00:00 UTC Dec 14 2023)" not in OSPF_Key_7:

                print( task.host.hostname + " , Key 7 needs to be updated" )
                writeToFile.writelines(task.host.hostname + " ,Key 7  is WRONG, send lifetime (12:00:00 UTC Jun 16 2022) - (12:00:00 UTC Dec 14 2023)," + str(dateNow) + "\n")
                #task.run(netmiko_send_config, config_file="C:\\Users\\""\\Desktop\\CONFIGS\\FIX.txt")

            else:
                print( task.host.hostname + "  ,Key 7 is correct 7 is OK ")
                writeToFile.writelines(task.host.hostname + " ,Key 7  is CORRECT, send lifetime (12:00:00 UTC Jun 16 2023) - (12:00:00 UTC Dec 14 2023)," + str(dateNow) + "\n")
        else:
            print(task.host.hostname + "  , Not running OSPF ")
            writeToFile.writelines(task.host.hostname  + "," + "Not Running OSPF" +"," + "," + str(dateNow) + "\n")

    except Exception as E:
        print(task.host.hostname + " TIMEOUT     " + str(E))
        writeToFile.writelines(task.host.hostname + " ,TIMEOUT "  +  str(E) + "," +  str(dateNow) + "\n")

    writeToFile.close()


results = nr.run(task=auto_config)

#print_result(results)
""

#import ipdb
#ipdb.set_trace()
