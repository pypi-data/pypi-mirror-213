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
import sys
import argparse
import logging
import logging.config
from functools import wraps

import utils

LOG = logging.getLogger('install')


def add_log(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            LOG.info("[INFO] Ascend DL deployed success --ascend-deployer")
            return result
        except Exception as e:
            print(e)
            LOG.error("[ERROR]Ascend DL deployed failed --ascend-deployer")
            return -1

    return wrap


class CLI(object):
    def __init__(self, prog, desc, epilog=None):
        self.parser = argparse.ArgumentParser(
            prog=prog, description=desc, epilog=epilog, formatter_class=utils.HelpFormatter)
        self.parser.add_argument("--check", dest="check", action="store_true", default=False, help="check environment")
        self.parser.add_argument("--clean", dest="clean", action="store_true", default=False,
                                 help="clean resources on remote servers")
        self.parser.add_argument("--nocopy", dest="no_copy", action="store_true", default=False,
                                 help="do not copy resources to remote servers when install for remote")
        self.parser.add_argument("--force_upgrade_npu", dest="force_upgrade_npu", action="store_true", default=False,
                                 help="can force upgrade NPU when not all devices have exception")
        self.parser.add_argument("--tensorflow_version", dest="tensorflow_version", choices=["1.15.0", "2.6.5"],
                                 default="1.15.0",
                                 help="Appoint tensorflow version,must be 1.15.0 or 2.6.5,default is 1.15.0")
        self.parser.add_argument("--verbose", dest="verbose", action="store_true", default=False, help="Print verbose")
        self.parser.add_argument("--ls", dest="ls", action="store_true", default=False,
                                 help="Show all packages version")
        self.parser.add_argument("--output-file", dest="output_file",
                                 help="Redirect the output of ansible execution results to a file")
        self.parser.add_argument("--install", dest="install", nargs="+", choices=utils.install_items,
                                 metavar="<package_name>", help="Install specific package: %(choices)s")
        self.parser.add_argument("--stdout_callback", dest="stdout_callback",
                                 help="set display plugin, e.g. ansible_log")
        self.parser.add_argument("--install-scene", dest="scene", nargs="?", choices=utils.scene_items,
                                 metavar="<scene_name>", help="Install specific scene: %(choices)s")
        self.parser.add_argument("--patch", dest="patch", nargs="+", choices=utils.patch_items,
                                 metavar="<package_name>", help="Patching specific package: %(choices)s")
        self.parser.add_argument("--patch-rollback", dest="patch_rollback", nargs="+", choices=utils.patch_items,
                                 metavar="<package_name>", help="Rollback specific package: %(choices)s")
        self.parser.add_argument("--test", dest="test", nargs="+", choices=utils.test_items, metavar="<target>",
                                 help="test the functions: %(choices)s")

    def run(self):
        args = self.parser.parse_args(utils.args_with_comma(sys.argv[1:]))
        if not any([args.install, args.scene, args.patch, args.patch_rollback, args.test, args.check, args.clean,
                    args.ls]):
            print("expected one valid argument at least")
            self.parser.print_help()
            return 1
        if args.install and args.scene:
            print("Unsupported --install and --install-scene at same time")
            return 1

        if args.stdout_callback:
            os.environ['ANSIBLE_STDOUT_CALLBACK'] = args.stdout_callback

        import jobs

        ansible_args = ['-v'] if args.verbose else []
        if args.check:
            check_tags = args.install if args.install else []
            if args.scene:
                check_tags.append(args.scene)
            return jobs.process_check(check_tags, no_copy=True, ansible_args=ansible_args)
        for handler, tags in (
                (jobs.process_install, args.install),
                (jobs.process_scene, args.scene),
                (jobs.process_patch, args.patch),
                (jobs.process_patch_rollback, args.patch_rollback)):
            if not tags:
                continue
            if 'dl' in tags:  # only for support XX ugly implementation
                handler = add_log(handler)
            envs = {
                'hosts_name': 'worker',
                'tensorflow_version': args.tensorflow_version,
                'force_upgrade_npu': args.force_upgrade_npu,
            }
            return handler(tags, no_copy=args.no_copy, envs=envs, ansible_args=ansible_args)
        if args.test:
            envs = {'hosts_name': 'worker'}
            return jobs.process_test(args.test, envs=envs, ansible_args=ansible_args)
        if args.clean:
            run_args = ['worker', '-m', 'shell', '-a', 'rm -rf ~/resources.tar ~/resources']
            run_args.extend(ansible_args)
            return jobs.process_clean(run_args)
        if args.ls:
            envs = {'only_package': 'true'}
            return jobs.process_ls(None, envs=envs, ansible_args=ansible_args)


def main():
    logging.config.dictConfig(utils.LOGGING_CONFIG)
    cli = CLI(
        "ascend-deployer",
        "Manage Ascend Packages and dependence packages for specified OS"
    )
    cli.run()


if __name__ == '__main__':
    main()
