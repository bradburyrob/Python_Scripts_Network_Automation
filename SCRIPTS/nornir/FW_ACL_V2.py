from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):

    try:
        task.run(netmiko_send_command, command_string="sh run | s extended fw_acl" )
        task.host["inventory"] = task.run(netmiko_send_command, command_string="sh run | s extended fw_acl", use_textfsm=True).result

        resultString = str(task.host["inventory"])


        #print(type(resultsList), resultsList)

        if "ip access-list extended fw_acl" in resultString:
            print("ACL exist in router " + task.host.hostname )
        else:
            print(task.host.hostname + " DOES NOT have fw ACL applied, need to FIX!")
            f = open("ACL_Status.v2.txt", "a")
            ACL_Status = ( task.host.hostname + " DOES NOT have fw ACL applied, need to FIX!", "\n")
            f.writelines(ACL_Status)
            f.close()

    except:
        print(task.host.hostname + " failed to connect or pull data")


results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
