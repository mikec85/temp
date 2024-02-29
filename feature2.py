#!/usr/bin/env python

from nornir import InitNornir

from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_netmiko import netmiko_multiline
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_inspect import nornir_inspect
from nornir.core.task import Result, Task

nr = InitNornir(config_file="config.yaml")

def netmiko_add_interface(task,network, interface):
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    output = net_connect.config_mode()
    output += net_connect.send_command(f"interface {interface}", expect_string=r"#")
    output += net_connect.send_command(f"ip address {network} 255.255.255.0", expect_string=r"#")
    output += net_connect.send_command(f"ip helper-address 10.12.12.12", expect_string=r"#")
    output += net_connect.send_command(f"ip helper-address 10.14.14.14", expect_string=r"#")
    output += net_connect.exit_config_mode()
    return output

# Function to add interface, set ip address and dhcp helper addressess
def add_interface(host,network,interface):
    cmh_hosts = nr.filter(name=host)
    result = cmh_hosts.run(task=netmiko_add_interface, network=network, interface=interface)

    if result[host].failed:
        return False

    return True

# Function to Check if a network route exists in the route table
def check_route(host,network):
    cmh_hosts = nr.filter(name=host)
    result = cmh_hosts.run(task=netmiko_send_command, command_string=f"show ip route | inc {network}")

    if "directly connected" in result[host].result:
        return True

    return False



