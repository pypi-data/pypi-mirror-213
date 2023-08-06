#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================
import os
import subprocess
import sys


IP_RULE_TEMPLATE = "ip_rule_%s=add from %s table %s\n"
IP_ROUTE_TEMPLATE = "ip_route_%s=add %s via %s dev eth%s table %s\n"
ADDRESS_TEMPLATE = """address_%s=%s
netmask_%s=%s
netdetect_%s=%s
"""
ROCE_PORT_TEMPLATE = "roce_port_%s=%s\n"
ARP_SEND_TEMPLATE = "send_arp_status_%s=%s\n"
DSCP_TC_TEMPLATE = "dscp_tc_%s=%s\n"
BITMAP_TEMPLATE = "bitmap_%s=%s\n"

GATEWAY_TEMPLATE = "gateway_%s=%s\n"
ARP_TEMPLATE = "arp_%s=-i eth%s -s %s %s\n"

RET_ERROR_CODE = -1
FIRST_CARD_IN_SECOND_GROUP = 4
FIRST_GROUP = (0, 1, 2, 3)
SECOND_GROUP = (4, 5, 6, 7)


def main(param):
    if ' ' in param:
        print("parm not right, exit...")
        raise Exception("param not right")
    param = param.split("-")
    param_number = 8
    if len(param) == param_number:
        ips, netdetect_ips, gateways, netmask, roce_port, bitmap, dscp_tc, common_network = param
    else:
        print("parm size not right, exit...")
        raise Exception("param size not right")
    
    gateway_count = len(set(gateways.split(',')))
    info = {}
    gateway_set = set()
    for _id, (ip, netdetect_ip) in enumerate(zip(ips.split(','), netdetect_ips.split(','))):
        matching_gateway, matching_network = get_gateway(ip, gateways, netmask)
        gateway_set.add(matching_gateway)
        info[_id] = {
            'id': _id, 'ip': ip, 'common_network': common_network, 'sub_network': matching_network, 
            'netdetect': netdetect_ip, 'gateway': matching_gateway
        }
    if len(gateway_set) == 1:
        full_connection = True
    else:
        full_connection = False
    common_info = {'netmask': netmask, 'roce_port': roce_port, 'dscp_tc': dscp_tc, 'bitmap': bitmap}
    content = get_content(common_info, info, gateway_count, full_connection)
    mode = 0o600
    fid = os.open("/etc/hccn.conf", os.O_RDWR | os.O_CREAT | os.O_TRUNC, mode)
    try:
        os.write(fid, content.encode('utf-8'))
    finally:
        os.close(fid)

    code, out = get_statusoutput("hccn_tool -a -cfg recovery")
    print(out)
    if code != 0:
        print("recovery hccn failed!")
        raise Exception("calling for hccn_tool failed")


def get_content(common_info, info, gateway_count, full_connection):
    content = ""
    macs = {}
    table_start = 104
    for dev_id in info.keys():
        err_code, mac = get_statusoutput('hccn_tool -i %s -mac -g' % dev_id)
        if not err_code:
            mac = mac.replace("mac addr: ", "").strip()
            macs[dev_id] = mac
    for dev_id in info.keys():
        table_id = table_start + int(dev_id)
        _info = info.get(dev_id, {})
        content += get_basic_defines(common_info, _info, dev_id)
        content += get_gateway_defines(gateway_count, _info, dev_id)
        if not full_connection:
            continue

        content += IP_RULE_TEMPLATE % (dev_id, _info.get('ip'), table_id)
        content += IP_ROUTE_TEMPLATE % (dev_id, _info.get("common_network"), _info.get("gateway"), dev_id, table_id)
        content += IP_ROUTE_TEMPLATE % (dev_id, _info.get("sub_network"), _info.get("ip"), dev_id, table_id)

        for other_dev_id in info.keys():
            if int(dev_id) < SECOND_GROUP[0]:
                group = FIRST_GROUP
            else:
                group = SECOND_GROUP
            if other_dev_id not in group or dev_id == other_dev_id:
                continue
            content += ARP_TEMPLATE % (dev_id, other_dev_id, info.get(other_dev_id, {}).get("ip"),
                                       macs.get(other_dev_id))
        content += ARP_SEND_TEMPLATE % (dev_id, 1)
    return content


def get_gateway_defines(gateway_count, _info, dev_id):
    content = ""
    if gateway_count > 1:
        if dev_id in (FIRST_GROUP[-1], SECOND_GROUP[-1]):
            content += GATEWAY_TEMPLATE % (dev_id, _info.get('gateway'))
    else:
        content += GATEWAY_TEMPLATE % (dev_id, _info.get('gateway'))
    return content


def get_basic_defines(common_info, _info, dev_id):
    content = ADDRESS_TEMPLATE % (dev_id, _info.get("ip"), dev_id, common_info.get("netmask"),
                                  dev_id, _info.get("netdetect"))
    content += ROCE_PORT_TEMPLATE % (dev_id, common_info.get("roce_port"))
    if common_info.get("dscp_tc").strip():
        content += DSCP_TC_TEMPLATE % (dev_id, common_info.get('dscp_tc'))
    if common_info.get("bitmap").strip():
        content += BITMAP_TEMPLATE % (dev_id, common_info.get("bitmap"))
    return content


def ip_to_int(ip):
    oct_multiper = 8
    return sum(int(octet) << (oct_multiper * i) for i, octet in enumerate(reversed(ip.split('.'))))


def mask_to_cidr(mask):
    return sum(bin(int(octet)).count('1') for octet in mask.split('.'))


def is_ip_in_subnet(ip, gateway_ip, subnet_mask):
    ip_int = ip_to_int(ip)
    gateway_ip_int = ip_to_int(gateway_ip)
    subnet_mask_int = ip_to_int(subnet_mask)
    return (ip_int & subnet_mask_int) == (gateway_ip_int & subnet_mask_int)


def get_subnet(gateway_ip, subnet_mask):
    subnet_prefix_length = mask_to_cidr(subnet_mask)
    gateway_ip_octets = [int(octet) for octet in gateway_ip.split(".")]
    subnet_mask_octets = [int(octet) for octet in subnet_mask.split(".")]
    network_address_octets = [gateway_ip_octets[i] & subnet_mask_octets[i] for i in range(4)]
    network_address = ".".join([str(octet) for octet in network_address_octets])
    subnet = "{}/{}".format(network_address, subnet_prefix_length)
    return subnet


def get_gateway(_ip, gateways, netmask):
    for gateway in gateways.split(','):
        network = get_subnet(gateway, netmask)
        if is_ip_in_subnet(_ip, gateway, netmask):
            return gateway, network

    return "", ""


def get_statusoutput(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    stdout, stderr = process.communicate()
    return_code = process.returncode
    stdout_str = stdout.decode('utf-8')
    stderr_str = stderr.decode('utf-8')
    return return_code, stdout_str + stderr_str


if __name__ == "__main__":
    err_existing = False
    try:
        if len(sys.argv) != 2:
            raise Exception("param size not right")
        main(sys.argv[1])
    except Exception as e:
        print("error happen!")
        print(e)
        err_existing = True
    if err_existing:
        sys.exit(RET_ERROR_CODE)
