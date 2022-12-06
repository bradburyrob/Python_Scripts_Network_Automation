from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command
import datetime


nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input("Enter Password: ")

def auto_config(task):
    dateNow = datetime.date.today()
    writeToFile = open("DHCP_Snooping_Implementation.csv","a")
    Router_Name = task.host.hostname
    try:

        task.host["VLAN10_INTERFACE"] = task.run(netmiko_send_command, command_string="show ip int brief  | in Vlan10").result
        VLAN10_INT = str(task.host["VLAN10_INTERFACE"]).split()[0]
        VLAN10_INT_IP_ADDRESS = str(task.host["VLAN10_INTERFACE"]).split()[1]

        print(task.host.hostname, VLAN10_INT, VLAN10_INT_IP_ADDRESS)

        task.host["VLAN_10_Config"] = task.run(netmiko_send_command, command_string="show run interface " +VLAN10_INT + " | inc ip address", use_textfsm=True).result
        INT_VL10_SHOW_RUN = str(task.host["VLAN_10_Config"]).split(" ")

        IPs_IN_VLAN10_INTERFACE = []
        for IP in INT_VL10_SHOW_RUN:
            if "1" in  IP:
                IPs_IN_VLAN10_INTERFACE.append(IP)
        print(IPs_IN_VLAN10_INTERFACE)

        task.host["VLAN_10_ARPs"] = task.run(netmiko_send_command, command_string="show ip arp  " + VLAN10_INT, use_textfsm=True).result
        INT_VL10_ARPs = task.host["VLAN_10_ARPs"]
        VLAN10_MAC_ADDRESS = ""
        Filtered_switch_IPs = []
        for arp in INT_VL10_ARPs:
            switch_IP = arp['address']
            if  VLAN10_INT_IP_ADDRESS ==  arp['address']:
                VLAN10_MAC_ADDRESS = arp['mac']
                print(VLAN10_MAC_ADDRESS)
            if switch_IP not in IPs_IN_VLAN10_INTERFACE:
                Filtered_switch_IPs.append(switch_IP)
        print(Filtered_switch_IPs)

        import netmiko
        for switch in Filtered_switch_IPs:
            try:
                switch_connection = netmiko.ConnectHandler(ip=switch, device_type="cisco_ios", username=nr.inventory.defaults.username ,password=nr.inventory.defaults.password, fast_cli=False)

                switch_name = str(switch_connection.send_command("show run | i hostname")).split(" ")[1]
                DHCP_Snooping_State = str(switch_connection.send_command("show ip dhcp snooping | i Switch DHCP snooping is")).split(" ")[4]

                if "vg" in switch_name or "VG" in switch_name or "voip" in switch_name or "r1" in switch_name or "enabled" in DHCP_Snooping_State or "c2" in switch_name:
                    pass  # Do nothing! Skip the VGs, Routers or Switches that already have DHCP Snooping enabled!
                else:
                    Ping_Router = str(switch_connection.send_command("ping " + VLAN10_INT_IP_ADDRESS))
                    FIND_Trusted_Port = str(switch_connection.send_command(
                        "show mac address address " + VLAN10_MAC_ADDRESS + " vlan 10")).split("\n")[5]
                    Trusted_PORT_Found = str(FIND_Trusted_Port).split(" ")
                    for item in Trusted_PORT_Found:
                        if "/" in item:
                            Trusted_PORT = item

                    print(switch_name, Trusted_PORT)
                    writeToFile.writelines(
                        Router_Name + "," + VLAN10_INT + "," + VLAN10_INT_IP_ADDRESS + "," + VLAN10_MAC_ADDRESS + "," + switch_name + "," + switch + "," + Trusted_PORT + "," + str(
                            dateNow) + "\n")
                    commands = ["ip dhcp snooping",
                                "no ip dhcp snooping information option",
                                "ip dhcp snooping vlan 101,201",
                                "interface " + Trusted_PORT,
                                "ip dhcp snooping trust",
                                "do wr"]
                    switch_connection.send_config_set(commands)

                    switch_connection.disconnect

            except netmiko.ssh_exception.NetMikoTimeoutException as  SSH_Error:
                print(switch, "could not SSH into switch SSH ERROR")
                writeToFile.writelines(Router_Name + "," + VLAN10_INT + "," + VLAN10_INT_IP_ADDRESS + "," + VLAN10_MAC_ADDRESS + "," + "Switch unreachable" + "," + switch + "," + "SSH Error TCP connection failed" + "," + str(dateNow) + "\n")

            except IndexError as ListIndexError:
                print(switch, "could not SSH into switch 1st", ListIndexError)
                writeToFile.writelines(
                    Router_Name + "," + VLAN10_INT + "," + VLAN10_INT_IP_ADDRESS + "," + VLAN10_MAC_ADDRESS + "," + "Switch unreachable" + "," + switch + "," + str(ListIndexError) + "," + str(dateNow) + "\n")

            except Exception as myError:
                print(switch, "could not SSH into switch", myError)
                writeToFile.writelines(
                    Router_Name + "," + VLAN10_INT + "," + VLAN10_INT_IP_ADDRESS + "," + VLAN10_MAC_ADDRESS + "," + "Switch unreachable" + "," + switch + "," + str(myError) + "," + str(dateNow) + "\n")

            except:
                print("not sure what happened")


    except Exception as E:
        print(Router_Name + " " + E)
        writeToFile.writelines(Router_Name + "," + "Could not connect" + ","  + ","+   "," + "," + "," + str(E) + ","+   str(dateNow) + "\n")

results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
