from flask import Flask, request, jsonify

from feature1 import *
from feature2 import *
from feature3 import *
from feature4 import *
from feature5 import *

app = Flask(__name__)

# Example http://127.0.0.1:5000/get-user?host=r1&username=test
@app.route("/get-user", methods=["GET"])
def verify_user():
    host = request.args.get('host')
    username = request.args.get('username')
    status = validate_username_exists(host,username)
    return_data = [{'status': status}]
    return jsonify(return_data), 200

# Example http://127.0.0.1:5000/create-user?host=r1&username=test2&password=test2
@app.route("/create-user", methods=["GET"])
def create_user():
    host = request.args.get('host')
    username = request.args.get('username')
    password = request.args.get('password')
    status = True
    reason = ""
    if not add_user(host,username, password):
        status = False
        reason = "add user failure"
    if not validate_username_exists(host,username):
        status = False
        reason = "User not exist"
    if not validate_connect(host,username, password):
        status = False
        reason = "Login test failure"

    return_data = [{'status': status, 'reason': reason}]
    return jsonify(return_data), 200

# Example http://127.0.0.1:5000/remove-user?host=r1&username=test2&password=test2
@app.route("/remove-user", methods=["GET"])
def remove_user_api():
    host = request.args.get('host')
    username = request.args.get('username')

    status = True
    if not remove_user(host,username):
        status = False

    return_data = [{'status': status}]
    return jsonify(return_data), 200

# Example http://127.0.0.1:5000/add-int?host=r1&network=10.1.1.1&interface=Loopback2
@app.route("/add-int", methods=["GET"])
def add_int():
    host = request.args.get('host')
    network = request.args.get('network')
    interface = request.args.get('interface')

    status = True
    reason = ""
    if not add_interface(host, network, interface):
        status = False
        reason = "Failed to add"
    if not check_route(host,network):
        status = False
        reason = "Failed route check"

    return_data = [{'status': status, 'reason': reason}]
    return jsonify(return_data), 200

# Example http://127.0.0.1:5000/find-mac?host=r1&mac=01:80:C2:00:00:0A,01:80:C2:00:00:0B
"""
Example output
[
  {
    "mac-address": "01:80:C2:00:00:0A",
    "switchport": "",
    "uplink_switch_name": "r1"
  },
  {
    "mac-address": "01:80:C2:00:00:0B",
    "switchport": "",
    "uplink_switch_name": "r1"
  }
]
"""
@app.route("/find-mac", methods=["GET"])
def find_mac_api():
    mac = request.args.get('mac')
    host = request.args.get('host')

    status =  find_mac(host, mac)

    return jsonify(status), 200


# Example http://127.0.0.1:5000/verify-vlan?host=r1&vlan=2
@app.route("/verify-vlan", methods=["GET"])
def verify_vlan_api():
    vlan = request.args.get('vlan')
    host = request.args.get('host')

    status = validate_vlans_exists(host, vlan)

    return_data = [{'status': status}]
    return jsonify(return_data), 200

# Example http://127.0.0.1:5000/add-vlan?host=r1&vlan=2
@app.route("/add-vlan", methods=["GET"])
def add_vlan_api():
    vlan = request.args.get('vlan')
    host = request.args.get('host')

    status = add_vlan(host, vlan)

    return_data = [{'status': status}]
    return jsonify(return_data), 200

# Example http://127.0.0.1:5000/remove-vlan?host=r1&vlan=2
@app.route("/remove-vlan", methods=["GET"])
def remove_vlan_api():
    vlan = request.args.get('vlan')
    host = request.args.get('host')

    status = remove_vlan(host, vlan)

    return_data = [{'status': status}]
    return jsonify(return_data), 200


# Example http://127.0.0.1:5000/set-vlan?host=r1&vlan=2&interface=GigabitEthernet1
@app.route("/set-vlan", methods=["GET"])
def set_vlan_api():
    vlan = request.args.get('vlan')
    host = request.args.get('host')
    interface = request.args.get('interface')

    status = set_vlan(host, vlan, interface)

    return_data = [{'status': status}]
    return jsonify(return_data), 200


# Example http://127.0.0.1:5000/find-neighbors?host=r1
"""
Example output
[
  {
    "devicename": "CoreSW",
    "uplink_port": "GigabitEthernet2"
  },
  {
    "devicename": "test1.localdomain",
    "uplink_port": "GigabitEthernet1"
  }
]
"""
@app.route("/find-neighbors", methods=["GET"])
def find_neighbors_api():
    host = request.args.get('host')

    status =  get_neighbors(host)

    return jsonify(status), 200


if __name__ == "__main__":
    app.run(debug=True)

