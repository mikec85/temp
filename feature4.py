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

# Function to check if a vlan exists on a device
def validate_vlans_exists(host,vlan):
    cmh_hosts = nr.filter(name=host)
    result = cmh_hosts.run(task=napalm_get, getters=["get_vlans"])

    for output in result[host].result["get_vlans"]:
        if output == vlan:
            return True

    return False

# Function to add a vlan to a device
def add_vlan(host,vlan):
    cmh_hosts = nr.filter(name=host)
    cmd_string=f"vlan {vlan}"

    result = cmh_hosts.run(task=netmiko_send_config, config_commands=cmd_string)

    if result[host].failed:
        return False

    return True

# Function to remove a vlan from a device
def remove_vlan(host,vlan):
    cmh_hosts = nr.filter(name=host)
    cmd_string=f"no vlan {vlan}"

    result = cmh_hosts.run(task=netmiko_send_config, config_commands=cmd_string)

    if result[host].failed:
        return False

    return True

def netmiko_set_vlan(task,vlan, interface):
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    output = net_connect.config_mode()
    output += net_connect.send_command(f"interface {interface}", expect_string=r"#")
    output += net_connect.send_command(f"switchport access vlan {vlan}", expect_string=r"#")
    output += net_connect.exit_config_mode()
    return output

# Function to assign a vlan to a given interface
def set_vlan(host,vlan,interface):
    cmh_hosts = nr.filter(name=host)

    result = cmh_hosts.run(task=netmiko_set_vlan, vlan=vlan, interface=interface)

    if result[host].failed:
        return False

    return True

