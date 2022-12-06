from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from rich import print
import os
import requests
import json
import datetime
nr = InitNornir("config2.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input("Enter Password: ")

def auto_config(task):
    dateNow = datetime.date.today()
    writeToFile = open("BGP_NEIGHBORS_" + str(dateNow) + ".csv", "a")
    try:
        neighbors = task.run(netmiko_send_command, command_string="show ip bgp neighbor", use_textfsm=True)
        if "BGP not active" in neighbors.result:
            print(task.host.hostname + ", BGP NOT ACTIVE")
            Status = (task.host.hostname + ", BGP NOT ACTIVE"+ "\n")
            writeToFile.writelines(Status)
        else:
            task.host["facts"] = neighbors.result
            indexer = task.host["facts"]
            for index in indexer:
                neighbor = index["neighbor"]
                remote_as = index["remote_as"]
                bgp_state = index["bgp_state"]
                localhost_ip = index["localhost_ip"]
                remote_ip = index["remote_ip"]
                inbound_routemap = index["inbound_routemap"]
                outbound_routemap = index["outbound_routemap"]
                if remote_as == "650":
                    isp = "Verizon"
                elif remote_as == "139":
                    isp = "AT&T"
                print(task.host.hostname,neighbor,remote_as,bgp_state,localhost_ip,remote_ip,isp,inbound_routemap,outbound_routemap)

                Status = (task.host.hostname + ", " + bgp_state + ", " + localhost_ip + ", " + neighbor + ", " + remote_as + ", " + isp + ", " + inbound_routemap + ", " + outbound_routemap + "\n")
                writeToFile.writelines(Status)

    except:
        print(task.host.hostname + ", COULD NOT SSH / TIMEOUT")
        Status = (task.host.hostname + ", COULD NOT SSH / TIMEOUT" + "\n")
        writeToFile.writelines(Status)
results = nr.run(task=auto_config)

