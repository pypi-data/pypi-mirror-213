# -*- coding:UTF-8 -*-
import unittest
import os
from halring.windows.halring_os import OsUtil


class TestOsUtil(unittest.TestCase):

    def test_os_util_001_file_exists(self):
        test_path = "test_os_util.py"
        OsUtil().get_file_md5(test_path)

    def test_os_util_002_file_isfile(self):
        test_path = "test_os_util.py"
        OsUtil().isfile(test_path)

    def test_os_util_003_file_isHidden(self):
        test_path = "test_os_util.py"
        OsUtil().isHidden(test_path)

    def test_os_util_004_file_copyFile(self):
        src_path = "test_os_util.py"
        dst_path = "new.py"
        OsUtil().copyFile(src_path, dst_path)

    def test_os_util_005_file_copyDir(self):
        src_dir = "..\\logs"
        dst_dir = "..\\newlogs"
        OsUtil().copyDir(src_dir, dst_dir)

    def test_os_util_006_file_get_file_md5(self):
        test_path = "test_os_util.py"
        OsUtil().get_file_md5(test_path)

    def test_os_util_007_check_rename(self):
        test_path = "D:\\GitRepos\\NGAir\\xls_file\\数据缓存\\NWF2020\\BPC_10.10.10\\5\\a.ini"
        os_util = OsUtil()
        print(os_util.check_rename(test_path,"-"))

    def test_os_util_008_check_rename(self):
        os_util = OsUtil()
        print(os_util.getNameDict("D:\\GitRepos\\NGAir\\xls_file\\数据缓存\\NWF2020\\BPC_10.10.10\\5\\a.ini"))

    def test_os_util_009_mkdir(self):
        os_util = OsUtil()
        os_util.mkdir("D:\\GitRepos\\NGAir\\\\xls_file\\数据缓存\\NWF2020\\BPC_10.10.10\\10\\编译\\比较\\from_dev\\")

    def test_os_util_010_delete(self):
        os_util = OsUtil()
        os_util.removeDirs("D:\\GitRepos\\NGAir\\xls_file\\数据缓存\\项目代码仓库\\bpc_FileTransport_Gateway",True)

    def test_os_util_svn_cmd_read(self):
        svncmd = 'svn list "http://svn.tc.com/BPMSrc/BMS/branches/CI/bms/" --recursive  --username cvsopuser --password Dev#Op6ser --no-auth-cache'
        result = os.popen(svncmd)
        res = result.read()
        print(str(res))

    def test_get_cmd_encode_type(self):
        os_util = OsUtil()
        print(os_util.get_cmd_encode_type())

