import json
import csv
import os.path
import sys


def solve_value_list(value_list):
    ret = ""
    for index, v in enumerate(value_list):
        if type(v) == dict:
            str_item = ''
            for key, value in v.items():
                if key == 'name':
                    str_item += value
                if key == 'version':
                    str_item += (":" + value)
            value_list[index] = str_item
    ret += "\n".join(value_list)
    return ret


def main(path):
    with open(path) as f:
        data = json.load(f)
        dir_name = os.path.dirname(path)
        ips = list(data.keys())

        fieldsname = ["IP", "npu", "packages", "HCCN info", "node name", "node type", "status", "ok pods",
                      "missing pods", "failed pods", "npu resource name in K8s", "images", "dl result"]
        flags = os.O_WRONLY | os.O_CREAT
        with os.fdopen(os.open(dir_name + '/report.csv', flags, 0o644), 'w', newline='') as wf:
            writer = csv.DictWriter(wf, fieldnames=fieldsname)
            writer.writeheader()
            for ip in ips:
                row = [ip]
                npu = data.get(ip, {}).get('npu', '')
                packages = solve_value_list(data.get(ip, {}).get('packages', []))
                hccn_info = data.get(ip, {}).get('hccn', '')
                node_name = data.get(ip, {}).get('node name', '')
                node_type = data.get(ip, {}).get('node type', '')
                status = data.get(ip, {}).get('status', '')
                ready_pods = "\n".join(data.get(ip, {}).get('ready pods', []))
                missing_pods = "\n".join(data.get(ip, {}).get('missing pods', []))
                failed_pods = "\n".join(data.get(ip, {}).get('failed pods', []))
                npu_cap = "\n".join(data.get(ip, {}).get('npu in K8s', []))
                images = "\n".join(data.get(ip, {}).get('images', []))
                result = data.get(ip, {}).get('dl result', '')
                row.extend(
                    [npu, packages, hccn_info, node_name, node_type, status, ready_pods, missing_pods, failed_pods,
                     npu_cap, images, result])
                writer.writerow(dict(zip(fieldsname, row)))


if __name__ == '__main__':
    main(sys.argv[1])
