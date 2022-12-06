from nornir import InitNornir
from nornir_netmiko import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_command

nr = InitNornir("config.yaml")

nr.inventory.defaults.username = ""
nr.inventory.defaults.password = input('Enter your Password:')

def auto_config(task):

    try:
        task.run(netmiko_send_command, command_string="sh ip eigrp neigh" )
        task.host["inventory"] = task.run(netmiko_send_command, command_string="sh ip eigrp neig", use_textfsm=True).result
        tunnels = task.host["inventory"]
        if len(tunnels) == 2:
            for tunnel in tunnels:
                firstTunnel     = tunnels[0]['interface']
                secondTunnel    = tunnels[1]['interface']
                firstNeighbor   = tunnels[0]['address']
                secondNeighbor  = tunnels[1]['address']

            print( task.host.hostname + " has neighbor "  + firstNeighbor  + " for " +      firstTunnel + " and " + secondNeighbor + " for " +  secondTunnel)

            f = open("DMVPN_Single_Hub_Check.v1.txt", "a")
            tunnalStatus1 = (task.host.hostname + " has neighbor "  + firstNeighbor  + "  " +      firstTunnel + " | " + secondNeighbor + "  " +  secondTunnel + "\n")
            f.writelines(tunnalStatus1)
            f.close()

        elif len(tunnels) == 3:
            for tunnel in tunnels:
                firstTunnel     = tunnels[0]['interface']
                secondTunnel    = tunnels[1]['interface']
                thirdTunnel    = tunnels[2]['interface']
                firstNeighbor   = tunnels[0]['address']
                secondNeighbor  = tunnels[1]['address']
                thirdNeighbor  = tunnels[2]['address']

            print( task.host.hostname + " has neighbor "  + firstNeighbor  + " for " +      firstTunnel + " and " + secondNeighbor + " for " +  secondTunnel + " and " + thirdNeighbor + " for tunnel" + thirdTunnel)

            f = open("DMVPN_Single_Hub_Check.v1.txt", "a")
            tunnalStatus1 = (task.host.hostname + " has neighbor "  + firstNeighbor  + "  " +      firstTunnel + " | " + secondNeighbor + " for " +  secondTunnel + " | " + thirdNeighbor + " " + thirdTunnel + "\n")
            f.writelines(tunnalStatus1)
            f.close()

        elif len(tunnels) == 1:
            for tunnel in tunnels:
                firstTunnel     = tunnels[0]['interface']
                firstNeighbor   = tunnels[0]['address']


            print( task.host.hostname + " has neighbor "  + firstNeighbor  + " for " +      firstTunnel)
            f = open("DMVPN_Single_Hub_Check.v1.txt", "a")
            tunnalStatus1 = (task.host.hostname + " has neighbor "  + firstNeighbor  + "  " +      firstTunnel +   "\n")
            f.writelines(tunnalStatus1)
            f.close()

    except:
        print(task.host.hostname + " failed to connect or pull data")
        tunnalStatus3 = (task.host.hostname + " did not connect to router" + "\n")
        f.writelines(tunnalStatus3)
        f.close()


results = nr.run(task=auto_config)

#print_result(results)


#import ipdb
#ipdb.set_trace()
