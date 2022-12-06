
from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):
    output_file = open("Generic_SFP_list.v99.csv", "a")
    task.run(netmiko_send_command, command_string="show inventory")
    task.host["inventory"] = task.run(netmiko_send_command, command_string="show inventory", use_textfsm=True).result

    inventory_items = task.host["inventory"]
   #
    for item in inventory_items:
        SFP_Name        = item['name']
        SFP_Desciption  = item['descr']
        SFP_PID         = item['pid']
        SW_Model = inventory_items[0]['descr']

        if "SFP" in SFP_Desciption :
            print(task.host.hostname + " Name " + SFP_Name + " Description " + SFP_Desciption + " PID " + SFP_PID + " Switch Model " + SW_Model)
            output_file.writelines(task.host.hostname + ", Name ," + SFP_Name + " , Description," + SFP_Desciption + " ,PID ," + SFP_PID  + ", Switch Model, " + SW_Model + "\n")

    output_file.close()


results = nr.run(task=auto_config)

print_result(results)


