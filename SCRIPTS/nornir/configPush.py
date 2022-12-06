from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')
def auto_config(task):
    try:
      task.run(netmiko_send_config,config_file="FIX.txt")
      print(task.host.hostname, "config sent")
    except:
       print(task.host.hostname, " could not SSH ----------")


results = nr.run(task=auto_config)
#results = nr.run(task=auto_config)
#print_result(results)
