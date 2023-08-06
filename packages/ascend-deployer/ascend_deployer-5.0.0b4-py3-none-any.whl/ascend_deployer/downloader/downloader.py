#!/usr/bin/env python3
# coding: utf-8
# Copyright 2020 Huawei Technologies Co., Ltd
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
"""downloader"""
import glob
import os
import sys
import argparse
from functools import wraps
from io import StringIO

from . import download_util
from . import logger_config
from . import pip_downloader
from . import os_dep_downloader
from . import other_downloader
from . import software_mgr
from . import dl_mef_dependency_downloader
from . import deb_downloader
from . import rpm_downloader
from .download_util import get_download_path, State, Color, get_free_space_b

FILE_PATH = os.path.realpath(__file__)
CUR_DIR = os.path.dirname(__file__)

LOG = logger_config.LOG
LOG_OPERATION = logger_config.LOG_OPERATION
MAX_DOWNLOAD_SIZE = 20 * (2 ** 30)


class DependencyDownload(object):
    def __init__(self, os_list, software_list, download_path, check):
        self.origin_download = None
        self.origin_cann_download = None
        self.progress = 0
        self.download_items = []
        self.dst = download_util.get_download_path()
        self.res_dir = os.path.join(self.dst, "resources")
        self.finished_items = []
        self.extra_schedule = None
        self.origin_check_download_hash = None
        self.origin_check_hash = None
        self.origin_print = print
        self.software_list = software_list
        self.download_path = download_path
        if check:
            self.check_software_list(os_list, software_list)
        if os.name == 'nt':
            os.system('chcp 65001')
            os.system('cls')

    @staticmethod
    def check_space(download_path):
        free_size = get_free_space_b(download_path)
        if free_size < MAX_DOWNLOAD_SIZE:
            print(Color.warn("[WARN] the disk space of {} is less than {:.2f}GB".format(download_path,
                                                                                        MAX_DOWNLOAD_SIZE / (
                                                                                                1024 ** 3))))

    @staticmethod
    def check_software_list(os_list, software_list):
        """
        check the download software list
        :param os_list: download os list
        :param software_list: download software list
        """
        check_stat, msg = download_util.check_version_matched(os_list, software_list)
        if check_stat == State.EXIT:
            print("[ERROR] {}".format(msg))
            LOG.error("[ERROR] {}".format(msg))
            sys.exit(1)
        if check_stat == State.ASK:
            print("[WARN] {}".format(msg))
            while True:
                answer = input("need to force download or not?(y/n)")
                if answer in {'y', 'yes'}:
                    print("Versions do not match, force download.")
                    LOG.info("Versions do not match, force download.")
                    break
                elif answer in {'n', 'no'}:
                    print("Versions do not match, exit.")
                    LOG.info("Versions do not match, exit.")
                    sys.exit(0)
                else:
                    print("Invalid input, please re-enter!")

    @staticmethod
    def process_bar(blocknum, blocksize, totalsize):
        recv_size = blocknum * blocksize
        # config scheduler
        f = sys.stdout
        pervent = recv_size / totalsize
        if pervent > 1:
            pervent = 1
        percent_str = "{:.2f}%".format(pervent * 100)
        n = round(pervent * 50)
        s = ('=' * (n - 1) + '>').ljust(50, '-')
        if pervent == 1:
            s = ('=' * n).ljust(50, '-')
        f.write('\r' + Color.info('All Download Progress:').ljust(61, ' ') +
                percent_str.ljust(7, ' ') + '[' + s + ']')
        f.flush()

    @staticmethod
    def download_other_packages(os_list, dst=None):
        """
        download other resources, such as source code tar ball
        """
        return other_downloader.download_other_packages(os_list, dst)

    @staticmethod
    def download_specified_python(dst=None):
        """
        download ascend_python_version=Python-3.7.5
        """
        return other_downloader.download_specified_python(dst)

    @staticmethod
    def download_other_software(os_list, software_list, dst):
        """
        download other resources, such as CANN and MindStudio
        """
        return other_downloader.download(os_list, software_list, dst)

    @staticmethod
    def download_python_packages(os_list, res_dir):
        """
        download_python_packages
        """
        return pip_downloader.download(os_list, res_dir)

    @staticmethod
    def download_mindspore(os_list, software_list, dst):
        """
        download_mindspore
        """
        return other_downloader.download_ms(os_list, software_list, dst)

    @staticmethod
    def download_torch_npu(os_list, software_list, dst):
        """
        download_torch_npu
        """
        return other_downloader.download_torch_npu(os_list, software_list, dst)

    @staticmethod
    def download_os_packages(os_list, software_list, dst):
        """
        download_os_packages
        """
        os_dep = os_dep_downloader.OsDepDownloader()
        return os_dep.download(os_list, software_list, dst)

    @staticmethod
    def download_dl_mef_resources(os_list, software_list, dst):
        """
        download_dl_mef_resources
        """
        for pkg_name in software_list:
            if "DL" in pkg_name or "MEF" in pkg_name:
                return dl_mef_dependency_downloader.download_dl_mef_dependency(os_list, software_list, dst)
        return {'ok': [], 'failed': []}

    @staticmethod
    def cursor_down():
        sys.stdout.write('\n')
        sys.stdout.flush()

    @staticmethod
    def cursor_up():
        sys.stdout.write('\x1b[1A')
        sys.stdout.flush()

    def mock_print(self, *args, **kwargs):
        # deal args with xxxErr
        if len(args) == 1 and not isinstance(*args, str):
            return print("\r", *args, **kwargs, end='')
        str_args = '\r' + Color.CLEAR + ''.join(list(args))
        return print(str_args, **kwargs, end='')

    def mock_download(self, *args, **kwargs):
        # mock other_downloader.DOWNLOAD_INST.download
        if args[1].endswith(".xml") or args[1].endswith("sqlite.bz2") or args[1].endswith("sqlite.xz"):
            self.download_items.append(args[0])
            return self.origin_download(*args, **kwargs)
        self.download_items.append(args[0])
        return True

    def mock_check_hash(self, *args, **kwargs):
        return True

    def collect_info(self, *args):
        self.check_space(self.download_path)
        msg = Color.info('start analyzing the amount of packages to be downloaded ...')
        self.origin_print(msg)
        LOG.info(msg, extra=logger_config.LOG_CONF.EXTRA)
        self.origin_download = other_downloader.DOWNLOAD_INST.download
        other_downloader.DOWNLOAD_INST.download = self.mock_download
        self.origin_check_download_hash = download_util.CH.check_download_hash
        download_util.CH.check_download_hash = self.mock_check_hash
        self.origin_check_hash = download_util.CH.check_hash
        download_util.CH.check_hash = self.mock_check_hash

        other_downloader.print = self.mock_print
        pip_downloader.print = self.mock_print
        download_util.print = self.mock_print
        os_dep_downloader.print = self.mock_print
        deb_downloader.print = self.mock_print
        rpm_downloader.print = self.mock_print
        dl_mef_dependency_downloader.print = self.mock_print
        origin_output = sys.stdout
        sys.stdout = StringIO()
        LOG.disabled = True
        pip_downloader.LOG.disabled = True
        os_dep_downloader.LOG.disabled = True
        deb_downloader.LOG.disabled = True
        rpm_downloader.LOG.disabled = True
        other_downloader.LOG.disabled = True
        dl_mef_dependency_downloader.LOG.disabled = True
        try:
            self.download_all(*args)
        except Exception as e:
            raise e
        finally:
            sys.stdout = origin_output
            LOG.disabled = False
            pip_downloader.LOG.disabled = False
            os_dep_downloader.LOG.disabled = False
            deb_downloader.LOG.disabled = False
            rpm_downloader.LOG.disabled = False
            other_downloader.LOG.disabled = False
            dl_mef_dependency_downloader.LOG.disabled = False

            print = self.origin_print
            download_util.CH.check_download_hash = self.origin_check_download_hash
            download_util.CH.check_hash = self.origin_check_hash
            pip_downloader.my_pip.downloaded = []
            other_downloader.DOWNLOAD_INST.download = self.counter(self.origin_download)
        msg = f'finish analyzing ...'
        print(msg)
        LOG.info(msg, extra=logger_config.LOG_CONF.EXTRA)

    def counter(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            finally:
                self.finished_items.append(args[0])
                self.cursor_down()
                self.process_bar(len(set(self.finished_items)), 1, len(set(self.download_items)))
                self.cursor_up()

        return wrap

    def download_all(self, os_list, software_list, dst):
        """
        download all resources
        """
        res_dir = os.path.join(dst, "resources")
        self.download_specified_python(dst)
        self.download_python_packages(os_list, res_dir)
        self.download_mindspore(os_list, software_list, dst)
        self.download_torch_npu(os_list, software_list, dst)
        self.download_os_packages(os_list, software_list, res_dir)
        self.download_other_packages(os_list, dst)
        self.download_other_software(os_list, software_list, dst)
        self.download_dl_mef_resources(os_list, software_list, dst)


def parse_argument(download_path):
    """
    解析参数
    """
    support_os_list = os.listdir(os.path.join(download_path, 'downloader', 'config'))
    support_pkg_list = os.listdir(os.path.join(download_path, 'downloader', 'software'))
    os_list_help = 'for example: --os-list=<OS1>,<OS2>\nSpecific OS list to download, supported os are:\n'
    for osname in sorted(support_os_list):
        os_list_help += '{}\n'.format(osname)
    download_help = 'for example: --download=<PK1>,<PK2>==<Version>\n' \
                    'Specific package list to download, supported packages are:\n'
    for pkg in sorted(support_pkg_list):
        pkg_name, version = pkg.split('_')
        download_help += '{}=={}\n'.format(pkg_name, version[:-5])

    parser = argparse.ArgumentParser(
        epilog="  notes: When <Version> is missing, <PK> is the latest.\r\n",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--os-list', action='store', dest='os_list',
                        help=os_list_help)
    parser.add_argument('--download', action='store', dest='packages',
                        help=download_help)

    try:
        args = parser.parse_args()
    except SystemExit as e:
        if e.code == 0:
            sys.exit(0)
        else:
            sys.exit(1)

    if args.os_list is None and args.packages is None:
        parser.print_help()
        sys.exit(0)

    if args.os_list is None or args.packages is None:
        print("os_list or packages can not be none")
        parser.print_help()
        sys.exit(0)

    if args.os_list is not None:
        for os_item in args.os_list.split(','):
            if os_item not in support_os_list:
                print('os {} is not supported'.format(os_item))
                parser.print_help()
                sys.exit(1)
    if args.packages is not None:
        for soft in args.packages.split(','):
            if not software_mgr.is_software_support(soft):
                print('software {} is not supported'.format(soft))
                parser.print_help()
                sys.exit(1)

    return args


def delete_glibc(os_list, download_path):
    delete_os_list = ['Kylin_V10Tercel_aarch64', 'Kylin_V10Tercel_x86_64']
    for i in delete_os_list:
        if i in os_list:
            os_dir = os.path.join(download_path, 'resources', i)
            glibc = glob.glob('{}/glibc-[0-9]*'.format(os_dir))
            try:
                os.unlink(glibc[0])
            except IndexError:
                pass


def main():
    """
    entry for console
    """
    download_path = get_download_path()
    try:
        args = parse_argument(download_path)
    except SystemExit as e:
        if e.code == 1:
            download_status = "Failed"
            exit_status = 1
        else:
            download_status = "Success"
            exit_status = 0
        log_msg = "downloading {}: {}".format(
            " ".join(sys.argv[1:]), download_status)
        LOG_OPERATION.info(log_msg, extra=logger_config.LOG_CONF.EXTRA)
        sys.exit(exit_status)

    os_list = []
    if args.os_list is not None:
        os_list = args.os_list.split(',')
    software_list = []
    if args.packages is not None:
        software_list = args.packages.split(',')
    download_dependency(os_list, software_list, download_path, args.force_download)


def download_dependency(os_list, software_list, download_path, check):
    download_status = "Failed"
    err_log = ""
    dependency_download = DependencyDownload(os_list, software_list, download_path, check)
    try:
        dependency_download.collect_info(os_list, software_list, download_path)
        dependency_download.download_all(os_list, software_list, download_path)
    except (KeyboardInterrupt, SystemExit):
        download_status = "Failed"
        err_log = Color.error("download failed,keyboard interrupt or system exit,please check.")
    except download_util.DownloadError as e:
        download_status = "Failed"
        err_log = Color.error("download failed,download from {} to {} failed".format(e.url, e.dst_file))
    except download_util.DownloadCheckError as e:
        download_status = "Failed"
        err_log = Color.error("{} download verification failed".format(e.dst_file))
    except Exception as e:
        download_status = "Failed"
        err_log = Color.error("download failed with error {} ,please retry.".format(e))
    else:
        download_status = "Success"
        err_log = ""
    finally:
        download_result = "\ndownload and check --os_list={} --download={}:{}".format(",".join(os_list),
                                                                                      ",".join(software_list),
                                                                                      download_status)
        if download_status == "Success":
            log_msg = "\n" + err_log + download_result
        else:
            log_msg = "\n\n" + err_log + download_result
        print(log_msg)
        LOG_OPERATION.info(log_msg, extra=logger_config.LOG_CONF.EXTRA)
        delete_glibc(os_list, download_path)


if __name__ == "__main__":
    main()
