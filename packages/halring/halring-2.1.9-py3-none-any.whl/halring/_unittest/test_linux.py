# -*- coding:UTF-8 -*-
import unittest
from halring.linux.halring_linux import LinuxUtil
linux_auth = ("jenkins-server-1", "10.112.6.14", "root", "#Sseadmin123")


class TestLinux(unittest.TestCase):

    def setUp(self):
        self.linux_cli = LinuxUtil(*linux_auth)

    def test_a_connect(self):
        try:
            self.linux_cli.connect_to_host()
        except:
            connect = False
        else:
            connect = True
        self.assertTrue(connect)

    def test_b_check_host_sftp_connect(self):
        result = self.linux_cli.check_host_sftp_connect()
        print(result)
        self.assertEqual(result["SFTP连接状态"], "正常")

    def test_c_python_version(self):
        result = self.linux_cli.check_host_python_version()
        print(f"c:[{result}]")
        self.assertEqual(result["python版本"], "未安装python运行环境")

    def test_d_check_host_java_vesion(self):
        result = self.linux_cli.check_host_java_vesion()
        print(f"d:[{result}")
        self.assertEqual(result["java version"], "未安装java运行环境")

    def test_e_check_host_cpu_mem_disk_useable(self):
        result = self.linux_cli.check_host_cpu_mem_disk_useable()
        print(f"e:[{result}]")
        self.assertIsNotNone(result)

