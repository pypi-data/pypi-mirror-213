#!/usr/bin/env python3
# -*- coding:utf-8 -*-#

# -----------------------------------------------------
# Name:              test_ssh2_util
# Author:            lzhou
# DateTime:          2019/10/14 11:26
# Description:
# -----------------------------------------------------
import unittest
from halring.ssh2_con.halring_ssh2 import Ssh2Util


class TestSsh2Util(unittest.TestCase):

    def test_openvms_showrb_ins_001(self):
        ssh_tool = Ssh2Util('197.1.133.1', 'ngts_47', 'shanghai')
        ssh_tool.connect()
        ret = ssh_tool.read(7)
        ssh_tool.find_expect(ret, 'SELECTION :')
        ssh_tool.send('q')
        ret = ssh_tool.read()
        ssh_tool.find_expect(ret, 'CHOICE:')
        ssh_tool.send('e')
        ret = ssh_tool.read()
        ssh_tool.find_expect(ret, '\\)\\$')
        ssh_tool.send('nob')
        ssh_tool.send('MCR TOL$EXE:SHOWRB -INS 600000')
        ret = ssh_tool.read(3)
        ssh_tool.disconnect()
        assert ssh_tool.find_expect(ret, '= 600000')

    def test_openvms_showrb_ins_002(self):
        ssh_tool = Ssh2Util('197.1.133.1', 'ngts_47', 'shanghai')
        ssh_tool.connect()
        ret_out, ret_err, ret_status = ssh_tool.exec_command('MCR TOL$EXE:SHOWRB -INS 600000')
        ssh_tool.disconnect()
        assert ssh_tool.find_expect(ret_out, '证券代码        = 600000')

    def test_openvms_dev_level_001(self):
        ssh_tool = Ssh2Util('172.23.1.101', 'aqc01', 'NGTSCFG', port=22)
        ssh_tool.connect()
        result1 = ssh_tool.read(5)
        assert ssh_tool.find_expect(result1, "@DEV->")
        ssh_tool.send(r'def_level DEV')
        result1 = ssh_tool.read(5)
        ssh_tool.disconnect()
        assert ssh_tool.find_expect(result1, "H3-DEV")

    def test_linux_send_cd_and_ls(self):
        ssh_tool = Ssh2Util('198.2.74.1', 'nop_14', 'nop_14')
        ssh_tool.connect()
        ssh_tool.send('cd EzEI')
        ssh_tool.send('ls')
        ret = ssh_tool.read()
        ssh_tool.disconnect()
        assert ssh_tool.find_expect(ret, 'alterEzEIMcPort.sh')

    def test_linux_exec_command(self):
        ssh_tool = Ssh2Util('198.2.74.1', 'nop_14', 'nop_14')
        ssh_tool.connect()
        ret_out, ret_err, ret_status = ssh_tool.exec_command('ls')
        ssh_tool.disconnect()
        assert ssh_tool.find_expect(ret_out, 'EzEI')

    def test_read_line(self):
        ssh_tool = Ssh2Util('172.23.1.101', 'aqc01', 'NGTSCFG', port=22)
        ssh_tool.connect()
        def_level_expect = r"@DEV->|@WATER->|@REL->|@PROD->|@NEW->"
        if ssh_tool.read_line(def_level_expect, 5):
            ssh_tool.send(r"def_level DEV")
            ssh_tool.read_line("DEV", 5)
        ssh_tool.send("dir")
        result = ssh_tool.read_line()
        print(result[1])

    def test_finger(self):
        ssh_tool = Ssh2Util('172.23.1.101', 'aqc_atp', 'NGTSCFG', port=22)
        ssh_tool.connect()
        def_level_expect = r"@DEV->|@WATER->|@REL->|@PROD->|@NEW->"
        if ssh_tool.read_line(def_level_expect, 5):
            ssh_tool.send(r"finger aqc_atp")
            finger_result = ssh_tool.read(1)
            integ_dir = finger_result.split("Directory: ")[1].split("\r\n")[0].strip()[:-1] + "." + "ATP"
