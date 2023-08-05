# -*- coding:UTF-8 -*-
import unittest
from halring.linux.halring_linux import LinuxUtil
from halring.common.halring_common import CommonUtil


class TestLinuxUtil(unittest.TestCase):

    def test_check_host_cpu_mem_disk_useable_001_ok(self):
        lu = LinuxUtil("jenkins-server-2", "10.112.6.207", "root", "Fwq@glymm1")
        lu.connect_to_host()
        check_dict = lu.check_host_cpu_mem_disk_useable()
        CommonUtil().show_dict(check_dict, "check_dict")
        lu.disconnect_to_host()

    def test_check_host_java_vesion_002_ok(self):
        lu = LinuxUtil("jenkins-server-2", "10.112.6.207", "root", "Fwq@glymm1")
        lu.connect_to_host()
        check_java_version_dict = lu.check_host_java_vesion()
        CommonUtil().show_dict(check_java_version_dict, "check_java_version_dict")
        lu.disconnect_to_host()

    def test_check_host_java_vesion_003_ok(self):
        lu = LinuxUtil("jenkins-server-2", "10.112.6.207", "root", "Fwq@glymm1")
        lu.connect_to_host()
        check_java_version_dict = lu.check_host_java_vesion()
        CommonUtil().show_dict(check_java_version_dict, "check_java_version_dict")
        lu.disconnect_to_host()

    def test_check_host_python_version_003_ok(self):
        lu = LinuxUtil("jenkins-server-2", "10.112.6.207", "root", "Fwq@glymm1")
        lu.connect_to_host()
        check_python_version_dict = lu.check_host_python_version()
        CommonUtil().show_dict(check_python_version_dict, "check_python_version_dict")
        lu.disconnect_to_host()


if __name__ == '__main__':
    unittest.main()
