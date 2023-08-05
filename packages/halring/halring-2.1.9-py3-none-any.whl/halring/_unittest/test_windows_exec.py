# -*- coding:UTF-8 -*-
import os.path
import unittest
from halring.windows_exec.halring_exec import ExecUtil


class TestOsUtil(unittest.TestCase):

    def test_exec_001_block_execute(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "exe" + os.sep
        exec_util = ExecUtil("startEzSTEP " + path + 'jfrog.exe')
        exec_util.block_execute()

    def test_plink_002_non_block_execute(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "exe" + os.sep
        exec_util = ExecUtil("startEzSTEP " + path + 'jfrog.exe')
        exec_util.non_block_execute()