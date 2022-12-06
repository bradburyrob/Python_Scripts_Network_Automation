from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get

nr = InitNornir("config.yaml")
nr.inventory.defaults.username = ""
username = nr.inventory.defaults.username
nr.inventory.defaults.password = input("Enter Password:")
password = nr.inventory.defaults.password

def get_query(task):
    try:
        task_one = task.run(task=napalm_get, getters=["get_arp_table"])
        task_two = task.run(netmiko_send_command, command_string="show snmp location", use_textfsm=True)

        task.host["facts1"] = task_one.result
        task.host["facts2"] = task_two.result
        snmp_result = task.host["facts2"]
        print(task.host.hostname, "This is the snmp location " +snmp_result)
        query_result = task.host["facts1"]
        my_arps_data = query_result
        my_arps = my_arps_data['get_arp_table']

        f = open("hosts2.yaml", "a")
        arpList = ("---"  + "\n")
        f.writelines(arpList)
        f.close()

        x =1
        for my_arp in my_arps:

            if  ".10"  in  my_arp['interface'] and "101" not in my_arp['interface'] or "vla10" in my_arp['interface'] and "vlan101" not in my_arp['interface'] :

                gold = my_arp['ip']

                import netmiko
                try:
                    switch_connection = netmiko.ConnectHandler(ip=gold, device_type="cisco_ios", username=username, password=password,fast_cli= False)

                    switch_name = str(switch_connection.send_command("sh run | s hostname")).split(" ")
                    sw_snmp_loc = switch_connection.send_command("show snmp location")
                    if  not sw_snmp_loc:
                        switch_connection.send_config_set("snmp-server location " + snmp_result, "do wr mem")
                        switch_connection.send_config_set("do write memory")
                        print(switch_name[1], "this switch did not have SNMP LOC configured")
                        snmp_findings = open("no_snmp_location_configured.txt", "a")
                        snmp_findings.writelines(switch_name[1] + " this switch does not have SNMP LOC configured" + "\n")
                        snmp_findings.close()
                    else:
                        print(switch_name[1], gold, switch_connection.send_command("show snmp location"))
                        switch_connection.send_config_set("do wr mem")
                    switch_connection.disconnect
                except:
                    print("could not SSH into switch", gold)


    except:
        print("Could not connect to", task.host.hostname)

results_arp = nr.run(task=get_query)
#print_result(results_arp)

#import ipdb
#ipdb.set_trace()

