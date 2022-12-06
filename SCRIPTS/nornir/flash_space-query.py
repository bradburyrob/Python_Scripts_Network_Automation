from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
import csv
nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):

    task.run(netmiko_send_command, command_string="dir")
    task.host["inventory"] = task.run(netmiko_send_command, command_string="dir", use_textfsm=True).result

    inventory_items = task.host["inventory"]
   #ipdb>  pp nr.inventory.hosts[2]['inventory'][1]['total_size']
    #'1624104960'
    #ipdb> pp nr.inventory.hosts[2][''][1]['total_free']


    flash_total_space_int  =int(inventory_items[1]['total_size'])/1000000
    flash_free_space_int=int(inventory_items[1]['total_free'])/1000000
    flash_used_space_int =  flash_total_space_int - flash_free_space_int
    flash_space_left_percentage = flash_free_space_int  / flash_total_space_int * 100

    print(task.host.hostname , " has this much total space in in megabytes "  , int(flash_total_space_int) , ", this much used space " , int(flash_used_space_int) , ", with this much free space " , int(flash_free_space_int), ", this percent left " , int(flash_space_left_percentage) ,"%")
    output_file = open("flash_space.csv", "a")
    output_file.writelines(task.host.hostname + " has this much total space in in megabytes, "  + str(flash_total_space_int) + ", this much used space, " + str(flash_used_space_int) + ", with this much free space, " + str(flash_free_space_int)+ ", this percent left, " + str(flash_space_left_percentage) +"%")
    output_file.writelines("\n")
    output_file.close()
    #print(type(flash_total_space) + " Lets cast to float" + type(float(flash_total_space)))



results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
