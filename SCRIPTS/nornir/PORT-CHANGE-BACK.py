#!/usr/nin/env python
from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
import os, datetime,rich
import csv
nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):
    dateNow = datetime.date.today()
    writeToFile = open("ROLLBACK_LOG-3-" + str(dateNow) + ".csv", "a")
    try:

        print(task.host.hostname)
        with open('VLAN_800_SHUTDOWN_PORTS_FIX.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    originalSwitch      = row[0]
                    originalPort        = row[1]
                    originalVlan        = row[2]

                    if   not row[3] or row[3] == "  ":
                        originalDescription = "//DATA USERS//"
                    else:
                        originalDescription = row[3]

                    if task.host.hostname == originalSwitch:
                        print(originalSwitch,originalPort,originalVlan,originalDescription)
                        task.run(netmiko_send_config, config_commands=["interface " + originalPort,
                                                                       "description " + originalDescription,
                                                                       "switchport access vlan " + originalVlan,
                                                                       "description " + originalDescription ,
                                                                       "spanning-tree portfast",
                                                                       "spanning-tree bpduguard enable",
                                                                       "switchport voice vlan 201",
                                                                       "trust device cisco-phone",
                                                                       "auto qos voip cisco-phone",
                                                                       "service-policy input AutoQos-4.0-CiscoPhone-Input-Policy",
                                                                       "service-policy output AutoQos-4.0-Output-Policy",
                                                                       "no shut"
                                                                       ])

                        
                        Status = (task.host.hostname + ", " + originalPort + ", " + originalVlan + ", " + originalDescription  + "\n")
                        writeToFile.writelines(Status)

                    #task.run(netmiko_send_config, config_commands=["write mem"])
                    line_count += 1
                else:
                    #print("not line 0")
                    line_count += 1
            #print(f'Processed {line_count} lines.')



    except:
        print(task.host.hostname + ", COULD NOT SSH / TIMEOUT")
        Status = (task.host.hostname + ", COULD NOT SSH / TIMEOUT" + "\n")
        #writeToFile.writelines(Status)


results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
