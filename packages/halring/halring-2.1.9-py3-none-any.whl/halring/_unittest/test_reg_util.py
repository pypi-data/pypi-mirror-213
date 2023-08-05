# coding=utf-8
import re
from halring.reg.halring_reg import RegUtil
import unittest


class TestRegUtil(unittest.TestCase):

    def test_reg_util_001_image_version_true(self):
        regutil = RegUtil()

        #version_regex = r"^[0-9a-zA-Z]+((\_(?!_))|(\_(?!\.))|(\_(?!\-))|(\.(?!\.))|(\.(?!\-))|(\.(?!\_))|(\-(?!\-))|(\-(?!\_))|(\-(?!\.))|[0-9a-zA-Z])+[0-9a-zA-Z]$"

        new_fixVersion_str = "ab5_cd4_ja3k"
        reg_result = regutil.reg_image_version(new_fixVersion_str)
        print(str(reg_result))
        assert reg_result == True

    def test_reg_util_002_image_version_true(self):
        regutil = RegUtil()
        new_fixVersion_str = "A5.2.3.1"
        reg_result = regutil.reg_image_version(new_fixVersion_str)
        print(str(reg_result))
        assert reg_result == True


    def test_reg_util_003_image_version_false(self):
        regutil = RegUtil()
        new_fixVersion_str = "中文版本"
        reg_result = regutil.reg_image_version(new_fixVersion_str)
        print(str(reg_result))
        assert reg_result == False

    def test_reg_util_004_image_version_false(self):
        regutil = RegUtil()
        new_fixVersion_str = "AA 223344"
        reg_result = regutil.reg_image_version(new_fixVersion_str)
        print(str(reg_result))
        assert reg_result == False

    def test_reg_util_005_image_version_false(self):
        regutil = RegUtil()
        new_fixVersion_str = "A2__11"
        reg_result = regutil.reg_image_version(new_fixVersion_str)
        print(str(reg_result))
        assert reg_result == False

    def test_reg_util_006_match_true9(self):
        p = 'http://artifactory.test.com:8081/artifactory/DevRelease/LTNDTEST/&^$123fixversion7+A=/'
        str1 = 'http://artifactory.test.com:8081/artifactory/DevRelease/LTNDTEST/&^$123fixversion7+A=/升级手册/'

        match_result =re.match("^"+p+".*$",str1)
        search_result = re.search(p,str1)
        aa = p in str1
        bb = str1.startswith(p)
        print(str(match_result))
        print(str(search_result))
        print(str(aa))
        print(str(bb))