from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from rich import print
import os
import requests
import json, time
nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input("Enter Password: ")

configFile = open("\\CONFIGS\\SNMP.txt")

def auto_config(task):
    try:
        task.run(netmiko_send_config, config_commands=configFile)
        time.sleep(2)
        print(task.host.hostname)
    except Exception as E:
        print(task.host.hostname + E)


results = nr.run(task=auto_config)
#import ipdb
#ipdb.set_trace()
