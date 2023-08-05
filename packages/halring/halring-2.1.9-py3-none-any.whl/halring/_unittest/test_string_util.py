# coding=utf-8
import unittest
from halring.common.halring_string import StringUtil
from halring.common.halring_common import CommonUtil


class TestStringUtil(unittest.TestCase):
    """
    UnitTest
    Author: xqzhou
    """
    def test_string_util_001_replace_string_SPACE(self):
        input_orig_string = "asdf|324234|[SPACE]|sdf|ewrwer|gvfdgd|SPACE|sr23j23oi"
        input_selected_string = "[SPACE]"
        input_replace_string = " "

        util = StringUtil()
        util.string_replace(input_orig_string, input_selected_string, input_replace_string)

    def test_string_util_002_replace_string_double_space(self):
        input_orig_string = "asdf|324234|[SPACE][SPACE]|sdf|ewrwer|gvfdgd|SPACE|sr23j23oi"
        input_selected_string = "[SPACE]"
        input_replace_string = " "

        util = StringUtil()
        util.string_replace(input_orig_string, input_selected_string, input_replace_string)

    def test_string_util_003_replace_string_triple_space(self):
        input_orig_string = "asdf|324234|[SPACE][SPACE]|s[SPACE]f|ewrwer|gvfdgd|SPACE|sr23j23oi"
        input_selected_string = "[SPACE]"
        input_replace_string = " "

        util = StringUtil()
        util.string_replace(input_orig_string, input_selected_string, input_replace_string)

    def test_string_util_004_string_diff_consisitency(self):
        input_left  = "abcd1234"
        input_right = "abcd1234"

        util = StringUtil()
        rtn = util.string_diff(input_left, input_right)
        print(rtn)
        assert rtn.__eq__(True)

    def test_string_util_005_string_diff_inconsisitency_rightmore(self):
        input_left  = "abcd1234"
        input_right = "abcd12345"

        util = StringUtil()
        rtn = util.string_diff(input_left, input_right)
        print(rtn)
        assert rtn.__eq__(False)

    def test_string_util_006_string_diff_inconsisitency_leftmore(self):
        input_left  = "abcd12345"
        input_right = "abcd1234"

        util = StringUtil()
        rtn = util.string_diff(input_left, input_right)
        print(rtn)
        assert rtn.__eq__(False)

    def test_string_util_007_string_diff_inconsisitency_leftright(self):
        input_left  = "abcd12345"
        input_right = "abcd54321"

        util = StringUtil()
        rtn = util.string_diff(input_left, input_right)
        print(rtn)
        assert rtn.__eq__(False)

    def test_string_util_008_step_autolen_ok(self):
        input_insert_step = "9=[STEP_AUTOLEN]35=D11=HBMY00100148=51988844=0.01038=10000054=1453=3448=A441005411452=5448=12994452=1448=12345452=400158=ZXQ"

        rtn = StringUtil().step_autolen(input_insert_step)
        print(rtn)
        assert rtn.__eq__("9=12235=D11=HBMY00100148=51988844=0.01038=10000054=1453=3448=A441005411452=5448=12994452=1448=12345452=400158=ZXQ")

    def test_string_util_009_step_null_ok(self):
        input_insert_step = "9=[STEP_AUTOLEN]35=D11=HBMY00100148=51988844=0.01038=[STEP_NULL]54=1453=3448=A441005411452=5448=12994452=1448=12345452=400158=ZXQ"

        rtn = StringUtil().step_null(input_insert_step)
        print(rtn)
        assert rtn.__eq__("9=[STEP_AUTOLEN]35=D11=HBMY00100148=51988844=0.01054=1453=3448=A441005411452=5448=12994452=1448=12345452=400158=ZXQ")

    def test_string_util_010_string_replace_space_ok(self):
        input_string = "9=[STEP_AUTOLEN]35=D11=HBMY00100148=51988844=0.01038=[STEP_NULL]54=1453=3448=A441005411452=5448=12994452=1448=12345452=400158=[SPACE]"

        rtn = StringUtil().string_replace_space(input_string)
        print(rtn)
        assert rtn.__eq__("9=[STEP_AUTOLEN]35=D11=HBMY00100148=51988844=0.01038=[STEP_NULL]54=1453=3448=A441005411452=5448=12994452=1448=12345452=400158= ")

    def test_string_util_011_string_replace_empty_ok(self):
        input_string = "9=[STEP_AUTOLEN]35=D11=[EMPTY]48=51988844=0.01038=[STEP_NULL]54=1453=3448=A441005411452=5448=12994452=1448=12345452=400158=[SPACE]"

        rtn = StringUtil().string_replace_empty(input_string)
        print(rtn)
        assert rtn.__eq__("9=[STEP_AUTOLEN]35=D11=48=51988844=0.01038=[STEP_NULL]54=1453=3448=A441005411452=5448=12994452=1448=12345452=400158=[SPACE]")

    def test_string_util_012_step_and_string_replace_combination_ok(self):
        input_string = "9=[STEP_AUTOLEN]35=D11=[EMPTY]48=51988844=0.01038=[STEP_NULL]54=1453=3448=A441005411452=5448=12994452=1448=12345452=400158=[SPACE]"

        string_util = StringUtil()
        input_string = string_util.string_replace_space(input_string)
        input_string = string_util.string_replace_empty(input_string)
        input_string = string_util.step_null(input_string)
        input_string = string_util.step_autolen(input_string)

        print(input_string)

    def test_string_util_013_step_ignore_info_ok(self):
        input_step = "9=134\x0160=20200107-15:18:15.123\x0142=20200107-15:20:34.789\x0117=4000000003\x0137=12\x01693=24\x0158=                                                  \x01                                                                                            "
        exp_step   = "9=X\x0160=YYYYMMDD-HH:MM:SS.000\x0142=YYYYMMDD-HH:MM:SS.000\x0117=X\x0137=X\x01693=X\x0158=                                                  \x01"
        string_util = StringUtil()
        print("befor [{0}]".format(input_step))
        rtn = string_util.step_ignore_info(input_step)
        print("after [{0}]".format(rtn))
        assert rtn.__eq__(exp_step)

    def test_string_util_014_string_diff_step_ok(self):
        input_left  = "9=23835=811=BPTAMPMY0737=3417=9000000348=12105031=7.00032=5000008504=35000000.000151=054=160=20070312-15:37:23.00042=20070312-15:37:22.000150=F39=2453=4448=D890013863452=5448=70003452=1448=A100000069452=39448=70003452=17"
        input_right = "9=23835=811=BPTAMPMY0737=3417=9000000348=12105031=7.00032=5000008504=35000000.000151=054=160=20070313-09:33:23.12342=20070313-09:34:01.349150=F39=2453=4448=D890013863452=5448=70003452=1448=A100000069452=39448=70003452=17"
        string_util = StringUtil()
        rtn = string_util.string_diff_step(input_left, input_right)
        print(rtn)
        assert rtn.__eq__(True)

    def test_string_util_015_string_diff_pubdata_ok(self):
        input_left  = "9=134\x0135=6\x0123=BIIAMPMY01\x0128=N\x0126= \x0148=121050\x0144=0.000\x0138=0\x0154=1\x01453=1\x01448=70003\x01452=1\x0158=                                                  \x01"
        input_right = "9=134\x0135=6\x0123=BIIAMPMY01\x0128=N\x0126= \x0148=121050\x0144=0.000\x0138=0\x0154=1\x01453=1\x01448=70003\x01452=1\x0158=                                                  \x01"
        string_util = StringUtil()
        rtn = string_util.string_diff_step(input_left, input_right)
        print(rtn)
        assert rtn.__eq__(True)

    def test_string_util_018_string_generate_ok_gen_X(self):
        string_util = StringUtil()
        rtn_string = string_util.string_generate("X", 1)
        print("rtn_string [{0}]".format(rtn_string))
        rtn_string = string_util.string_generate("X", 2)
        print("rtn_string [{0}]".format(rtn_string))
        rtn_string = string_util.string_generate("X", 4)
        print("rtn_string [{0}]".format(rtn_string))

    def test_string_util_019_string_generate_ok_gen_len(self):
        string_util = StringUtil()
        num = 1
        num_string_len = len(str(num))
        rtn_string = string_util.string_generate("A", num_string_len)
        print("rtn_string [{0}]".format(rtn_string))

        num = 17
        num_string_len = len(str(num))
        rtn_string = string_util.string_generate("B", num_string_len)
        print("rtn_string [{0}]".format(rtn_string))

        num = 123456789
        num_string_len = len(str(num))
        rtn_string = string_util.string_generate("C", num_string_len)
        print("rtn_string [{0}]".format(rtn_string))

    def test_string_util_020_string_generate_ok_gen_len_multi_string(self):
        string_util = StringUtil()
        rtn_string = string_util.string_generate("AB", 1)
        print("rtn_string [{0}]".format(rtn_string))
        rtn_string = string_util.string_generate("ABC", 2)
        print("rtn_string [{0}]".format(rtn_string))
        rtn_string = string_util.string_generate("A2B", 3)
        print("rtn_string [{0}]".format(rtn_string))

    def test_string_util_022_string_ignore_hex_zero_ok(self):
        input_string = "13027|CH1SHST12345|" + b'\x00'.decode() + "|" + b'\x00'.decode() + "|N||Y|N|N|Y"
        exp_string = "13027|CH1SHST12345|||N||Y|N|N|Y"
        string_util = StringUtil()
        rtn_string = string_util.string_ignore_hex_zero(input_string)
        assert rtn_string.__eq__(exp_string)

    def test_string_util_023_string_ignore_hex_zero_nok_no_hex_zero(self):
        input_string = "13027|CH1SHST12345| | |N||Y|N|N|Y"
        string_util = StringUtil()
        rtn_string = string_util.string_ignore_hex_zero(input_string)
        assert rtn_string.__eq__(input_string)

    def test_string_util_026_read_list_error_try_except(self):
        input_list = ""
        try:
            a = input_list[0]
        except Exception:
            print("catch input list [0] is error")
            input_list = "z"
            a = input_list[0]
            print("a="+a)
        assert a is "z"

    def test_string_from_list_with_delimiter_027_ok(self):
        orig_list = ["USER01$:[USER]", "USER02$:[USER]", "USER03$:[USER]", "USER04$:[USER]",
                     "USER05$:[USER]", "USER06$:[USER]", "USER07$:[USER]", "USER08$:[USER]",
                     "USER09$:[USER]", "USER10$:[USER]", "USER11$:[USER]", "USER12$:[USER]"]
        string_util = StringUtil()
        rtn_string = string_util.string_from_list_with_delimiter(orig_list)
        print("[OLD]{0}".format(orig_list))
        print("[NEW]{0}".format(rtn_string))

        rtn_string = string_util.string_from_list_with_delimiter(orig_list, '|')
        print("[OLD]{0}".format(orig_list))
        print("[NEW]{0}".format(rtn_string))

        rtn_string = string_util.string_from_list_with_delimiter(orig_list, ',')
        print("[OLD]{0}".format(orig_list))
        print("[NEW]{0}".format(rtn_string))

    def test_string_conv_list_to_str_028_ok(self):
        """
        ["AST591", "AST592", "AST593", "AST594"]
        TO
        'AST591', 'AST592', 'AST593', 'AST594'
        """
        orgi_list = ["AST591", "AST592", "AST593", "AST594"]
        item_prefix = "'"
        item_postfix = "'"
        item_delimiter = ", "
        rtn_str = StringUtil().string_conv_list_to_str(orgi_list, item_prefix, item_postfix, item_delimiter)
        CommonUtil().show_str(rtn_str, "rtn_str")

    def test_string_conv_list_to_str_029_ok(self):
        """
        ["AST591", "AST592"]
        TO
        host_info_idkey like '%AST591%' or host_info_idkey like '%AST592%'
        """
        orgi_list = ["AST591", "AST592", "AST593", "AST594"]
        item_prefix = "host_info_idkey like '%"
        item_postfix = "'"
        item_delimiter = " or "
        rtn_str = StringUtil().string_conv_list_to_str(orgi_list, item_prefix, item_postfix, item_delimiter)
        CommonUtil().show_str(rtn_str, "rtn_str")

    def test_string_ignore_single_quota_030_ok(self):
        input_str = "芝'陈"
        rtn_str = StringUtil().string_ignore_single_quota(input_str)
        CommonUtil().show_str(rtn_str, "rtn_str")

    def test_string_ignore_single_quota_030_ok_none_single_quota(self):
        input_str = "芝陈"
        rtn_str = StringUtil().string_ignore_single_quota(input_str)
        CommonUtil().show_str(rtn_str, "rtn_str")