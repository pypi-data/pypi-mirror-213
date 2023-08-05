# coding=utf-8
import unittest
from svn.halring_svn import SvnUtil


class TestRedisUtil(unittest.TestCase):

    def test_svn(self):
        input_user = "pei.xiaodong"
        input_pwd = "Qq.2921481"
        svn_cli = SvnUtil(input_user, input_pwd)
        svn_cli.svn_info('http://svn.tc.com/TOOLDoc/Lantern/3.%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86/Lantern_3.2.0/v3.2.0%E5%8F%98%E6%9B%B4%E7%82%B9%E7%9F%A9%E9%98%B5.xlsx')
        # redis连接

    def test_svn_2(self):
        input_user = "pei.xiaodong"
        input_pwd = "Qq.2921481"
        svn_cli = SvnUtil(input_user, input_pwd)
        svn_cli.svn_info_get_revision(
            'http://svn.tc.com/TOOLDoc/Lantern/3.%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86/Lantern_3.2.0/v3.2.0%E5%8F%98%E6%9B%B4%E7%82%B9%E7%9F%A9%E9%98%B5.xlsx'
        )

    def test_svn_3(self):
        input_user = "pei.xiaodong"
        input_pwd = "Qq.2921481"
        svn_cli = SvnUtil(input_user, input_pwd)
        svn_cli.svn_info_get_commit_id(
            'http://svn.tc.com/TOOLDoc/Lantern/3.%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86/Lantern_3.2.0/v3.2.0%E5%8F%98%E6%9B%B4%E7%82%B9%E7%9F%A9%E9%98%B5.xlsx'
        )

    def test_svn_4(self):
        input_user = "pei.xiaodong"
        input_pwd = "Qq.2921481"
        svn_cli = SvnUtil(input_user, input_pwd)
        svn_cli.svn_info_is_file_or_directory(
            'http://svn.tc.com/TOOLDoc/Lantern/3.%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86/Lantern_3.2.0/v3.2.0%E5%8F%98%E6%9B%B4%E7%82%B9%E7%9F%A9%E9%98%B5.xlsx'
        )