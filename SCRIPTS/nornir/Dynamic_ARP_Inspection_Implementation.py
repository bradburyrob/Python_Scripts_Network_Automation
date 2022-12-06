from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
import datetime

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = ""
#nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):
    dateNow = datetime.date.today()
    writeToFile = open("Dynamic_ARP_Inspection_Implementation.csv","a")
    Router_Name = task.host.hostname
    interfacePort = ""
    try:

        task.host["SNOOPING"] = task.run(netmiko_send_command, command_string="show ip dhcp snooping | in Switch DHCP snooping is" , use_textfsm=True).result
        task.host["CDP_Neighbors"] = task.run(netmiko_send_command, command_string="sh int status", use_textfsm=True).result

        Snooping_State =""
        if "enable" in str(task.host["SNOOPING"]):
            Snooping_State = "ENABLED"
            print(Router_Name,"Snooping is",Snooping_State)

            for item in task.host["CDP_Neighbors"]:
                if item['vlan'] == "trunk":
                    interfacePort = item['port']
                    print(Router_Name, " Interface that needs ARP trust enabled ", interfacePort)
                    task.run(netmiko_send_config, config_commands=["ip arp inspection vlan 101,201",
                                                                   "interface " + interfacePort,
                                                                   "ip arp inspection trust",
                                                                   "do wr"])
                    writeToFile.writelines(Router_Name + "," + "Interface needs to have ARP trust enabled" + "," + interfacePort + "," + "DHCP Snooping State," + Snooping_State + ","  + str(dateNow) + "\n")

        else:
            Snooping_State = "DISABLED"
            print(Router_Name,"Snooping is",Snooping_State)

    except Exception as myError:
        print("could not SSH into switch", myError)
        writeToFile.writelines(Router_Name +  "," +  + "," + "Switch unreachable" + "," +  + "," + myError +","+str(dateNow) + "\n")


results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
