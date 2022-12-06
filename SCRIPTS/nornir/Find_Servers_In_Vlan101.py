from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
import datetime


nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = ""

def auto_config(task):
    dateNow = datetime.date.today()
    writeToFile = open("Find_The_Servers_in_Vlan101.csv","a")
    Router_Name = task.host.hostname
    Filtered_host_IPs_DHCP_Snooping_Table = []
    try:

        neighbors = task.run(netmiko_send_command, command_string="sh cdp neigh", use_textfsm=True)
        task.host["facts"] = neighbors.result
        indexer = task.host["facts"]
        for index in indexer:
            local_int = index['local_interface']
            remoteInt = index['neighbor_interface']
            remoteDev = index['neighbor']
            remotePla = index['platform']
        #-------------------------------------------------------------------------------------
        task.host["VLAN101_INTERFACE"] = task.run(netmiko_send_command, command_string="show ip int brief  | in   (.*)0/0.101[ ]").result
        VLAN101_INT = str(task.host["VLAN101_INTERFACE"]).split()[0]
        VLAN101_INT_IP_ADDRESS = str(task.host["VLAN101_INTERFACE"]).split()[1]

        print(task.host.hostname, VLAN101_INT, VLAN101_INT_IP_ADDRESS)


        task.host["VLAN_101_Config"] = task.run(netmiko_send_command, command_string="show run interface " +VLAN101_INT + " | inc ip address", use_textfsm=True).result
        INT_VL101_SHOW_RUN = str(task.host["VLAN_101_Config"]).split(" ")

        IPs_IN_VLAN101_INTERFACE = []
        for IP in INT_VL101_SHOW_RUN:
            if "1" in  IP:
                IPs_IN_VLAN101_INTERFACE.append(IP)
        print(IPs_IN_VLAN101_INTERFACE)

        task.host["VLAN_101_ARPs"] = task.run(netmiko_send_command, command_string="show ip arp  " + VLAN101_INT, use_textfsm=True).result
        INT_VL101_ARPs = task.host["VLAN_101_ARPs"]
        VLAN101_MAC_ADDRESS = ""
        Filtered_host_IPs_ARP_Table = []
        for arp in INT_VL101_ARPs:
            host_IP = arp['address']
            if  VLAN101_INT_IP_ADDRESS ==  arp['address']:
                VLAN101_MAC_ADDRESS = arp['mac']
                print(VLAN101_MAC_ADDRESS)
            if host_IP not in IPs_IN_VLAN101_INTERFACE:
                Filtered_host_IPs_ARP_Table.append(host_IP)
        print("Hosts IPs from the ARP table:", end=" ")
        print(Filtered_host_IPs_ARP_Table)
        #--------------------------------------------------------------------------------------

        import netmiko,textfsm

        try:
            switch_connection = netmiko.ConnectHandler(ip=remoteDev, device_type="cisco_ios", username=nr.inventory.defaults.username ,password=nr.inventory.defaults.password, fast_cli=False)

            switch_name = str(switch_connection.send_command("show run | s hostname")).split(" ")[1]
            if "vg" in switch_name or "VG" in switch_name:
                pass # Do nothing! Skip the VGs!
            else:
                FIND_IPs_From_Snooping_Table = switch_connection.send_command("sh ip dhcp snooping binding vlan 101", use_textfsm=True)

                parseSnooping = open('C:\\Users\\r1acer1b\\Desktop\\Python\\ntc_templates\\templates\\cisco_ios_show_ip_dhcp_snooping.textfsm')
                fsm = textfsm.TextFSM(parseSnooping)
                result = fsm.ParseText(FIND_IPs_From_Snooping_Table)

                #IPs_From_Snooping_Table = str(FIND_IPs_From_Snooping_Table).split("\n")
                print("IPs from Snooping Table:     ", end=" ")
                for x in result:
                    if "IpAddress" in x[1] or "----"  in x[1]:
                        pass
                    else:
                        Filtered_host_IPs_DHCP_Snooping_Table.append(x[1])

                print(Filtered_host_IPs_DHCP_Snooping_Table)
                switch_connection.disconnect

                for item in Filtered_host_IPs_ARP_Table:
                    if item not in Filtered_host_IPs_DHCP_Snooping_Table:
                        print("This device has a static IP assigned " + item )
        except Exception as myError:
            print(switch_name,"could not SSH into switch", myError)

    except Exception as error:

        print(Router_Name + " failed to connect or pull data", error)
        writeToFile.writelines(Router_Name + "," + "Could not connect" + ","  + ","+   "," + "," + error +  "," + ","+   str(dateNow) + "\n")

results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
