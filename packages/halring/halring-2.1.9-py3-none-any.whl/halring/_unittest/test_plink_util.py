# coding=utf-8
import unittest
import re
from halring.plink.halring_plink import PlinkUtil


class TestPlinkUtil(unittest.TestCase):

    def test_plink_001_openvms_show_cpu(self):
        input_ip = "197.1.153.1"
        input_user = "ngts_53"
        input_pwd = "shanghai"
        input_cmd = "show cpu"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        plink.plink_execute()

    def test_plink_002_openvms_show_def(self):
        input_ip = "197.1.153.1"
        input_user = "ngts_53"
        input_pwd = "shanghai"
        input_cmd = "show def"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        plink.plink_execute()

    def test_plink_003_openvms_search_fpenvconf(self):
        input_ip = "197.1.153.1"
        input_user = "ngts_53"
        input_pwd = "shanghai"
        input_cmd = "search user_fpenvconf_file \"TCG_ENV_NAME\""
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        plink.plink_execute()

    def test_plink_004_linux_df(self):
        input_ip = "198.2.112.1"
        input_user = "nop_14"
        input_pwd = "nop_14"
        input_cmd = "df -h"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        plink.plink_execute()

    def test_plink_005_linux_netstat(self):
        input_ip = "198.2.112.1"
        input_user = "nop_14"
        input_pwd = "nop_14"
        input_cmd = "netstat"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        plink.plink_execute()

    def test_plink_006_openvms_chn_char(self):
        input_ip = "197.1.153.1"
        input_user = "ngts_53"
        input_pwd = "shanghai"
        input_cmd = "type back01$:[air.script]test_chn_char.txt"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute()
        print("[{0}]".format(rtn))

    def test_plink_007_openvms_showall_chn_char(self):
        input_ip = "197.1.153.1"
        input_user = "ngts_53"
        input_pwd = "shanghai"
        input_cmd = "mcr tol$exe:showall -brk -bk QNERNRSPR001 -repo"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute()
        print("[{0}]".format(rtn))

    def test_plink_008_openvms_plink_pipe(self):
        input_ip = "197.1.153.1"
        input_user = "ngts_53"
        input_pwd = "shanghai"
        input_cmd = "@BACK01$:[AIR.SCRIPT]RUN_WITH_INPUT.COM \\\"show dev dsa /unit=byte\\\" back01$:[air.script]startenv.script"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute()
        print("[{0}]".format(rtn))

    def test_plink_009_openvms_plink_pipe_replace(self):
        input_ip = "197.1.153.1"
        input_user = "ngts_53"
        input_pwd = "shanghai"
        input_cmd = "@BACK01$:[AIR.SCRIPT]RUN_WITH_INPUT.COM 'show dev dsa /unit=byte' back01$:[air.script]startenv.script"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute()
        print("[{0}]".format(rtn))

    def test_plink_010_openvms_plink_pipe_cmd(self):
        input_ip = "197.1.153.1"
        input_user = "ngts_53"
        input_pwd = "shanghai"
        input_cmd = "pipe show dev dsa | search sys$input dsa"
        input_cmd = "show dev dsa"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute()
        print("[{0}]".format(rtn))

    def test_plink_012_openvms_plink_biztool_chn(self):
        input_ip = "197.1.153.1"
        input_user = "ngts_53"
        input_pwd = "shanghai"
        input_cmd = "perl TOL$DCL:BIZTOOL.PL -m BIP*** OA2301000023100000TR2315000023590000"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute()
        print("[{0}]".format(rtn))

    def test_plink_013_openvms_plink_showall_search_long_result(self):
        input_ip = "197.1.56.1"
        input_user = "ngts_15"
        input_pwd = "shanghai"
        input_cmd = "sea  toff78$:[toff78.data.work]101ord.txt 2602040003"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute_vms()
        print("[{0}]".format(rtn))

    def test_plink_013_openvms_plink_ast593(self):
        input_ip = "172.2.11.1"
        input_user = "ngts_15"
        input_pwd = "shanghai"
        input_cmd = "show time"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute_vms()
        print("[{0}]".format(rtn))

    def test_plink_013_openvms_plink_hsd002(self):
        input_ip = "172.23.1.55"
        input_user = "aqc_diffmtp"
        input_pwd = "lantern"
        input_cmd = "show time"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute_vms()
        print("[{0}]".format(rtn))

    # --------------------- Down Need System Startup ---------------------------
    def test_plink_014_openvms_plink_showall_ins_biz_chn_new(self):
        input_ip = "197.1.56.1"
        input_user = "ngts_15"
        input_pwd = "shanghai"
        input_cmd = "mcr tol$exe:showall -ins -i 110981 -b bpt"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        try:
            rtn = plink.plink_execute()
        except:
            print("plink receive backend info error, try use plink_execute_vms")
            rtn = plink.plink_execute_vms()
        print("[{0}]".format(rtn))

    def test_plink_015_openvms_plink_showall_acc_ok(self):
        input_ip = "197.1.56.1"
        input_user = "ngts_15"
        input_pwd = "shanghai"
        input_cmd = "mcr tol$exe:showall -acc -a A102358939"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute()
        print("[{0}]".format(rtn))

    def test_plink_016_openvms_hex_zero_ok(self):
        input_ip = "197.1.56.1"
        input_user = "ngts_15"
        input_pwd = "shanghai"
        input_cmd = "mcr tol$exe:showall -pbu -p 13027"
        expect_rtn = "13027|CH1SHST12345|||N||Y|N|N|Y"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute_vms()
        no_hex_zero_rtn = ""
        for item in rtn:
            no_hex_zero_rtn = no_hex_zero_rtn + item.strip(b'\x00'.decode())
        print("======1=======[{0}]".format(rtn))
        print("======2=======[{0}]".format(no_hex_zero_rtn))
        print("======3=======[{0}]".format(expect_rtn))
        hex_zero = b'\x00'.decode()
        icld_hex_zero = "A" + hex_zero + "B"
        print("icld_hex_zero = [{0}]".format(icld_hex_zero))
        no_hex_zero = re.sub(hex_zero, "", icld_hex_zero)
        print("no_hex_zero   = [{0}]".format(no_hex_zero))
        assert expect_rtn in no_hex_zero_rtn

    def test_plink_017_openvms_copy_result_ok(self):
        input_ip = "197.1.56.1"
        input_user = "ngts_15"
        input_pwd = "shanghai"
        input_cmd = "CONV /FDL=TOFF$FDL:FPCONF_TRF.FDL USER_FPCONF_TRF_FILE USER_FPCONF_TRF_FILE /STAT"
        expct_rtn = "Total Valid Records:             112"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_execute()
        assert expct_rtn in rtn

    def test_plink_018_openvms_plink_mass_execute_ok(self):
        input_ip = "197.1.56.1|197.1.186.1"
        input_user = "ngts_15|ngts_15"
        input_pwd = "shanghai|shanghai"
        input_cmd = "show def"
        expct_rtn = "TOFF15$:[TOFF15.DATA.WORK]"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_mass_execute()
        print("exec_rtn ={}".format(rtn))
        print("expct_rtn={}".format(expct_rtn))
        assert expct_rtn in rtn

    def test_plink_018_openvms_plink_mass_execute_nok(self):
        input_ip = "197.1.56.1|197.1.186.1"
        input_user = "ngts_15|ngts_15"
        input_pwd = "shanghai|shanghai"
        input_cmd = "show cpu"
        expct_rtn = "HP Integrity BL870c i2"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        rtn = plink.plink_mass_execute()
        print("exec_rtn ={}".format(rtn))
        print("expct_rtn={}".format(expct_rtn))
        assert expct_rtn in rtn

    def test_plink_019_openvms_show_cpu_on_cst(self):
        input_ip = "198.2.40.1"
        input_user = "nop_15"
        input_pwd = "shanghai"
        input_cmd = "show cpu"
        plink = PlinkUtil(input_ip, input_user, input_pwd, input_cmd)
        plink.plink_execute()