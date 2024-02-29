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


def netmiko_direct_user(task,user):
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    output = net_connect.config_mode()
    output += net_connect.send_command(f"no username {user}", expect_string=r"confirm")
    output += net_connect.send_command("y", expect_string=r"#")
    output += net_connect.exit_config_mode()
    return output

# Function to validate User Exists
def validate_username_exists(host,username):
    cmh_hosts = nr.filter(name=host)
    result = cmh_hosts.run(task=napalm_get, getters=["get_users"])

    for output in result[host].result["get_users"]:
        if output == username:
            return True

    return False

# Function to add user login
def add_user(host,username,password):
    cmh_hosts = nr.filter(name=host)
    cmd_string=f"username {username} privilege 15 password {password}"

    result = cmh_hosts.run(task=netmiko_send_config, config_commands=cmd_string)

    if result[host].failed:
        return False

    return True

# Function to remove user
def remove_user(host,username):
    cmh_hosts = nr.filter(name=host)
    result = cmh_hosts.run(task=netmiko_direct_user, user=username)

    if result[host].failed:
        return False

    return True

# Function to login to device to validate credentials
def validate_connect(host,username,password):
    cmh_hosts = nr.filter(name=host)

    for host_obj in cmh_hosts.inventory.hosts.values():
        host_obj.username = username
        host_obj.password = password

    result = cmh_hosts.run(task=netmiko_send_command, command_string="show ip int br")

    if result[host].failed:
        return False

    return True




