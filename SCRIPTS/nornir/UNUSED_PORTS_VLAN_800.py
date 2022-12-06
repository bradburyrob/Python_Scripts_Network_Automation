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
    writeToFile = open("VLAN_800_" + str(dateNow) + "_SHUTDOWN_PORTS.csv","a")
    try:
        task.host["inventory"] = task.run(netmiko_send_command, command_string="show interface status", use_textfsm=True).result
        Devices = task.host["inventory"]
        for Device in Devices:
             vlan = str(Device['vlan'])
             name   = str(Device['name'])
             status   = str(Device['status'])
             port = str(Device['port'])
             if vlan != "trunk" and status == "notconnect":

                 lastInput = task.run(netmiko_send_command, command_string="show interface " + port + " | inc Last input", use_textfsm=True).result
                 lastInputValue = str(lastInput).split()
                 #print(task.host.hostname, port,  "input = ", lastInputValue[2],"output=",lastInputValue[4])
                 if "never" not in lastInputValue[2] and "never" not in lastInputValue[4]:
                     toDays = lastInputValue[2]

                     if "y" in toDays:
                         splitYears = toDays.split("y")
                         splitWeeks = splitYears[1].split("w")
                         yearsToDays = int(splitYears[0]) * 365
                         weeksTodays = (int(splitWeeks[0])*7)
                         totalDaysUnused = yearsToDays + weeksTodays
                         task.run(netmiko_send_config, config_commands=["vlan 800",
                                                                        "name NULL_VLAN",
                                                                        "default interface " + port,
                                                                        "interface " + port,
                                                                        "switchport access vlan 800",
                                                                        "description NOT USED",
                                                                        "shut",
                                                                        "do wr"])

                         print(task.host.hostname+ ", " + port + ", " + vlan + ",  "+ name + ", "+ status + ", " , totalDaysUnused )
                         Status = (task.host.hostname+ ", " + port + ", " + vlan + ",  "+ name + ", "+ status + ", " , str(totalDaysUnused)  + "\n")
                         writeToFile.writelines(Status)

                     elif "w" in toDays:
                         splitWeeks = toDays.split("w")
                         splitDays = splitWeeks[1].split("d")
                         daysCount = int(splitWeeks[0]) * 7 + int(splitDays[0])
                         if daysCount >= 30:
                             task.run(netmiko_send_config, config_commands=["vlan 800",
                                                                            "name NULL_VLAN",
                                                                            "default interface " + port,
                                                                            "interface " + port,
                                                                            "switchport access vlan 800",
                                                                            "description NOT USED",
                                                                            "shut",
                                                                            "do wr"])

                         print(task.host.hostname + ", " + port + ", " + vlan + ",  " + name + ", " + status + ", " , daysCount)
                         Status = (task.host.hostname + ", " + port + ", " + vlan + ",  " + name + ", " + status + ", " , str(daysCount) + "\n")
                         writeToFile.writelines(Status)

                     else:
                         print(task.host.hostname + ", " + port + ", " + vlan + ",  " + name + ", " + status + ", " , toDays)
                         Status = (task.host.hostname + ", " + port + ", " + vlan + ",  " + name + ", " + status + ", " , toDays + "\n")
                         writeToFile.writelines(Status)

                 elif "never" in lastInputValue[2] and "never" in lastInputValue[4]:
                     task.run(netmiko_send_config, config_commands=["vlan 800",
                                                                    "name NULL_VLAN",
                                                                    "default interface " + port,
                                                                    "interface " + port,
                                                                    "switchport access vlan 800",
                                                                    "description NOT USED",
                                                                    "shut",
                                                                    "do wr"])

                     print(task.host.hostname + ", " + port + ", " + vlan + ", " + name + ", " + status + ", ", lastInputValue[2] )
                     Status = (task.host.hostname + ", " + port + ", " + vlan + ",  " + name + ", " + status + ", ", lastInputValue[2] +"\n")
                     writeToFile.writelines(Status)

    except:
        print(task.host.hostname + " TIMEOUT")
        writeToFile.writelines(task.host.hostname + " ,TIMEOUT"  + "\n")

    writeToFile.close()

results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
