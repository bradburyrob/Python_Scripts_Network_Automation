from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):

    task.run(netmiko_send_command, command_string="show interface switchport",use_textfsm=True).result
    task.host["inventory"] = task.run(netmiko_send_command, command_string="sh interfaces switchport ", use_textfsm=True).result

#nr.inventory.hosts[1]['inventory'][1]['access_vlan']
#nr.inventory.hosts[33]['MAC'][0]['destination_address']
    inventory_items = task.host["inventory"]
   #
    for item in inventory_items:
        Interface_Name        = item['interface']
        Port_Vlan        = item['access_vlan']

        if( "301" in Port_Vlan):
            task.run(netmiko_send_command, command_string="  show mac address-table interface " + Interface_Name, use_textfsm=True).result
            task.host["MAC"] = task.run(netmiko_send_command, command_string="  show mac address-table interface " + Interface_Name,use_textfsm=True).result
            MACs = task.host["MAC"]
            for mac in MACs:
                dest_mac = mac['destination_address']
                print(task.host.hostname  +  " has the following interfaces  " + Interface_Name + " in VLAN " + Port_Vlan + "  mac address " + dest_mac)


                output_file = open("Printer_MACs.txt", "a")
                output_file.writelines(task.host.hostname + "   " + Interface_Name + " in VLAN " + Port_Vlan + "  mac address " + dest_mac)
                output_file.writelines("\n")
                output_file.close()

results = nr.run(task=auto_config)




#import ipdb
#ipdb.set_trace()
