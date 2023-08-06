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
import pathlib
import subprocess

import utils
from downloader.download_util import get_specified_python


class AnsibleJob(object):
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file

    @staticmethod
    def get_inventory_file():
        return pathlib.Path(utils.ROOT_PATH, 'inventory_file').as_posix()

    @staticmethod
    def handle_python_env(args):
        tar_name = get_specified_python()
        version = tar_name.replace('P', 'p').replace('-', '')
        args.extend([
            '-e', 'python_tar={}'.format(tar_name),
            '-e', 'python_version={}'.format(version),
        ])

    def run_playbook(self, tags, no_copy=False, envs=None, ansible_args=None):
        args = self.build_args(envs)
        skip_tags = []
        if tags:
            if not isinstance(tags, list):
                tags = [tags]
            if 'all' in tags:
                tags[tags.index('all')] = 'whole'  # all is ansible reserved tag
            if no_copy:
                skip_tags.append('copy')
            else:
                tags.append('copy')
            args.extend(['--tags', ','.join(tags)])
            if skip_tags:
                args.extend(['--skip-tags', ','.join(skip_tags)])
        if ansible_args:
            args.extend(ansible_args)
        return subprocess.run(args, shell=False, env=os.environ, check=True)

    def build_args(self, envs):
        inventory_file = self.get_inventory_file()
        args = ['ansible-playbook', '-i', inventory_file, self.yaml_file]
        if not envs:
            envs = {}
        self.handle_python_env(args)
        for k, v in envs.items():
            args.extend(['-e', '{}={}'.format(k, v)])
        return args

    def run_ansible(self, run_args):
        inventory_file = self.get_inventory_file()
        args = ['ansible', '-i', inventory_file]
        args.extend(run_args)
        return subprocess.run(args, shell=False, env=os.environ, check=True)


process_path = pathlib.Path(utils.ROOT_PATH, 'playbooks', 'process')
process_install = AnsibleJob(process_path.joinpath('process_install.yml').as_posix()).run_playbook
process_scene = AnsibleJob(process_path.joinpath('process_scene.yml').as_posix()).run_playbook
process_patch = AnsibleJob(process_path.joinpath('process_patch.yml').as_posix()).run_playbook
process_patch_rollback = AnsibleJob(process_path.joinpath('process_patch_rollback.yml').as_posix()).run_playbook
process_test = AnsibleJob(process_path.joinpath('process_test.yml').as_posix()).run_playbook
process_check = AnsibleJob(process_path.joinpath('process_check.yml').as_posix()).run_playbook
process_clean = AnsibleJob(None).run_ansible
process_ls = AnsibleJob(pathlib.Path(utils.ROOT_PATH, 'playbooks', 'report.yaml').as_posix()).run_playbook
process_hccn = AnsibleJob(pathlib.Path(utils.ROOT_PATH, 'playbooks', 'hccn.yaml').as_posix()).run_playbook
