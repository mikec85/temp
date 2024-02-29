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

# Function to get neighboring LLDP devices
def get_neighbors(host):
    cmh_hosts = nr.filter(name=host)
    result = cmh_hosts.run(task=napalm_get, getters=["get_lldp_neighbors"])

    lldpjson = []
    for output in result[host].result["get_lldp_neighbors"]:
        lldpjson.append({
            "devicename": result[host].result["get_lldp_neighbors"][output][0]["hostname"],
            "uplink_port": output
        })

    return(lldpjson)

