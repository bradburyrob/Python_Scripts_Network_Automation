from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
import datetime

currentDateNow = datetime.datetime.now()
nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):

    try:
        task.run(netmiko_send_command, command_string="sh run int 10 | i tunnel source" )
        task.host["inventory"] = task.run(netmiko_send_command, command_string="sh run int tu 10 | i tunnel source", use_textfsm=True).result

        resultString = str(task.host["inventory"])
        resultsList = resultString.split(sep=" ")

        for item in resultsList:
            if "net" in item:
                WAN_INTERFACE = item


        task.run(netmiko_send_command, command_string="sh run interface " + WAN_INTERFACE)
        task.host["ACL_Inventory"] = task.run(netmiko_send_command, command_string="sh run interface " + WAN_INTERFACE, use_textfsm=True).result
        Quering_Interface_for_ACL = task.host["ACL_Inventory"]
        if "fw_acl" in Quering_Interface_for_ACL:
            print(task.host.hostname + " has the ACL applied")

        else:
            print(str(currentDateNow) + "\t" + task.host.hostname + " DOES NOT have fw_acl ACL applied, need to FIX!", WAN_INTERFACE)

            f = open("ACL_Status.v1.txt", "a")
            ACL_Status = (str(currentDateNow)+ "\t" +  task.host.hostname + " DOES NOT have fw_acl ACL applied, need to FIX!", WAN_INTERFACE +  "\n")

            f.writelines(ACL_Status)

            '''
            task.run(netmiko_send_config,config_file="fw_acl.txt")
            task.run(netmiko_send_config, config_commands=["interface " + WAN_INTERFACE,
                                                            "ip access-group fw in" ,
                                                            "do wr"])
            '''

    except:
        print(task.host.hostname + " failed to connect or pull data",WAN_INTERFACE)

    f.close()
results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
