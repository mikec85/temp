#!/usr/bin/env python

from nornir import InitNornir
import json

from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir_netmiko import netmiko_multiline
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_inspect import nornir_inspect
from nornir.core.task import Result, Task

nr = InitNornir(config_file="config.yaml")

# Function to find the ports that a list of mac addresses are attached to
def find_mac(host,macaddress_to_scan):
    cmh_hosts = nr.filter(name=host)
    result = cmh_hosts.run(task=napalm_get, getters=["get_mac_address_table"])

    macjson = []

    for output in result[host].result["get_mac_address_table"]:
        for mac in macaddress_to_scan.split(","):
            if output["mac"] == mac:
                macjson.append({
                    "mac-address" : mac,
                    "uplink_switch_name" : host,
                    "switchport" : output["interface"]
                })

    return macjson

