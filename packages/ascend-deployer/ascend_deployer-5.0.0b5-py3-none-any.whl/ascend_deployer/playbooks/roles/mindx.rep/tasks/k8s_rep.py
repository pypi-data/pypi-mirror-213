import os.path
import subprocess
import json
import sys
from collections import OrderedDict

require_by_all = ["calico-node", "kube-proxy", ]
master_by_scene = {'1': ["etcd", "kube-apiserver", "kube-controller-manager", "kube-scheduler"],
                   '2': ["etcd", "kube-apiserver", "kube-scheduler"],
                   '3': ["etcd", "kube-apiserver", "kube-scheduler"],
                   '4': ["etcd", "kube-apiserver", "kube-controller-manager", "kube-scheduler", "ascend-cert",
                         "ascend-edge", "ascend-ngnix"]
                   }

all_master_together_by_scene = {'1': ["calico-kube-controllers", "coredns", "hccl-controller", "ascend-operator",
                                      " resilience-controller", "volcano-scheduler", "volcano-controllers"],
                                '2': ["calico-kube-controllers", "coredns",
                                      "volcano-scheduler", "volcano-controllers", ],
                                '3': ["calico-kube-controllers", "coredns"],
                                '4': ["calico-kube-controllers", "coredns"]
                                }
                                
worker_by_scene = {
    '1': ["ascend-device-plugin", "noded", "npu-exporter", ],
    '2': ["ascend-device-plugin", ],
    '3': ["ascend-device-plugin", ]
}


def get_type(master, worker):
    if master and worker:
        ret = "master,worker"
    elif master:
        ret = "master"
    else:
        ret = "worker"
    return ret


def get_status(conditions):
    return conditions[len(conditions) - 1].get("type", "")


def get_npu(capacity):
    devices = []
    for key, value in capacity.items():
        if "huawei" in key:
            devices.append("%s:%s" % (key, value))
    return devices


def get_images(images):
    ret = []
    for dic in images:
        ret.extend(dic.get("names", []))
    return ret


def get_nodes_info():
    result = subprocess.check_output(['kubectl', 'get', 'nodes', '-o', 'json'], encoding="utf-8")
    nodes_info = json.loads(result)
    nodes_dict = {}
    for node in nodes_info.get("items", {}):
        ip_address = node.get("status", {}).get("addresses", [])[0].get("address", "")
        property_dict = OrderedDict()
        property_dict['node name'] = node.get("status", {}).get("addresses", [])[1].get("address", "")
        property_dict['node type'] = get_type(node.get("metadata", {}).get("labels", {}).get("masterselector", ""),
                                              node.get("metadata", {}).get("labels", {}).get("workerselector", ""))
        property_dict['status'] = get_status(node.get("status", {}).get("conditions", []))
        property_dict['npu in K8s'] = get_npu(node.get("status", {}).get("capacity", {}))
        property_dict['images'] = get_images(node.get("status", {}).get("images", []))
        property_dict['ready pods'] = []
        property_dict['missing pods'] = []
        property_dict['failed pods'] = []
        nodes_dict[ip_address] = property_dict
    return nodes_dict


def get_pods_info(nodes_dict):
    result = subprocess.check_output(['kubectl', 'get', 'pods', '-A', '-o', 'json'], encoding="utf-8")
    pods_info = json.loads(result)
    for pod in pods_info.get("items", {}):
        ip = pod.get("status", {}).get("hostIP", "")
        property_dict = nodes_dict.get(ip, {})
        name = pod.get("metadata", {}).get("name", "")
        if pod.get("status", {}).get("phase", "") == "Running":
            property_dict.setdefault('ready pods', [])
            property_dict.get('ready pods', []).append(name)
        else:
            property_dict.setdefault('failed pods', [])
            property_dict.get('failed pods', []).append(name)

    return nodes_dict


def check_if_missing(info, require_list):
    already_pods = info.get("ready pods", [])
    for require_pod in require_list:
        flag = False
        for ready_pod in already_pods:
            if ready_pod.startswith(require_pod):
                flag = True
                break
        if not flag:
            info.get("missing pods", []).append(require_pod)


def missing_add_to_all_master(temp_dict, node_dict):
    for ip, info in node_dict.items():
        character = info.get("node type", "")
        if "master" in character:
            info.get("missing pods", []).extend(temp_dict.get("missing pods", []))


def check_missing_pods(node_dict, scene):
    all_master_pods = []
    for ip, info in node_dict.items():
        check_if_missing(info, require_by_all)
        character = info.get("node type", "")
        if "master" in character:
            require_list = master_by_scene.get(scene, [])
            check_if_missing(info, require_list)
            all_master_pods.extend(info.get("ready pods", []))
        if "worker" in character:
            require_list = worker_by_scene.get(scene, [])
            check_if_missing(info, require_list)
    temp_dict = {"ready pods": all_master_pods}
    check_if_missing(temp_dict, all_master_together_by_scene.get(scene, []))
    missing_add_to_all_master(temp_dict, node_dict)
    return node_dict


def is_dl_success(node_dict):
    for ip, info in node_dict.items():
        if info.get("status", "") != "Ready":
            return False
        if len(info.get("missing pods", [])) > 0:
            return False
        if len(info.get("failed pods", [])) > 0:
            return False
    return True


def append_result(node_dict, result):
    for ip, info in node_dict.items():
        info.setdefault("dl result", result)


def main(path_name, scene):
    node_dict = get_nodes_info()
    node_dict = get_pods_info(node_dict)
    node_dict = check_missing_pods(node_dict, scene)
    if is_dl_success(node_dict):
        append_result(node_dict, "success")
    else:
        append_result(node_dict, "failed")
    if os.path.isdir(path_name):
        flags = os.O_WRONLY | os.O_CREAT
        with os.fdopen(os.open(path_name + '/node_dict.json', flags, 0o700), 'w', newline='') as f:
            json.dump(node_dict, f)


if __name__ == '__main__':
    path = sys.argv[1]
    scene_num = sys.argv[2]
    main(path, scene_num)
