from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
import os, datetime
nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')
dateNow = datetime.date.today()


def auto_config(task):
    writeToFile = open("TELNET-v1.csv", "a")

    try:
        task.host["inventory"] = task.run(netmiko_send_command, command_string="sh run | sec line vty", use_textfsm=True).result

        resultString = str(task.host["inventory"])

        if "telnet" in resultString:
            print(task.host.hostname + " has telnet enabled in the VTY lines,violation")
            writeToFile.writelines(task.host.hostname + " ,has telnet enabled in the VTY lines, violation" + "\n")
            task.run(netmiko_send_config, config_commands=["line vty 0 15",
                                                           " transport input ssh" ,
                                                           " transport output ssh" ,
                                                           "do wr"])
        else:
            print(task.host.hostname + " DOES NOT Telnet enabled!, compliant ")
            writeToFile.writelines(task.host.hostname + " ,DOES NOT Telnet enabled!, compliant " + "\n")


    except:
        print(task.host.hostname + " failed to connect or pull data")
        writeToFile.writelines(task.host.hostname + " ,TIMEOUT,TIMEOUT"  + "\n")
        writeToFile.close()


results = nr.run(task=auto_config)


#print_result(results)


#import ipdb
#ipdb.set_trace()
