# coding=utf-8
import unittest
from halring.rds_lib.halring_rds_api import RdsApiUtil


class TestMySqlUtil(unittest.TestCase):

    def test_rds_util_001_backup(self):
        user = "ygong_uums"
        apisecret = "35ccbe94-f528-4f0f-86af-bb816056e15f"
        rdsid = "295"
        rds_util = RdsApiUtil("http://10.112.4.161:5526/api/", user, apisecret, rdsid)
        rds_util.create_backup("fxc")

    def test_rds_util_002_backup_db_not_exist(self):
        user = "ygong_uums"
        apisecret = "35ccbe94-f528-4f0f-86af-bb816056e15f"
        rdsid = "295"
        rds_util = RdsApiUtil("http://10.112.4.161:5526/api/", user, apisecret, rdsid)
        # message=“数据库aaa不存在”
        print(rds_util.create_backup("aaa"))


    def test_rds_util_003_list(self):
        user = "ygong_uums"
        apisecret = "35ccbe94-f528-4f0f-86af-bb816056e15f"
        rdsid = "295"
        rds_util = RdsApiUtil("http://10.112.4.161:5526/api/", user, apisecret, rdsid)
        print(rds_util.list_db_all_backup("fxc"))

    def test_rds_util_004_recovery(self):
        user = "ygong_uums"
        apisecret = "35ccbe94-f528-4f0f-86af-bb816056e15f"
        rdsid = "295"
        rds_util = RdsApiUtil("http://10.112.4.161:5526/api/", user, apisecret, rdsid)
        print(rds_util.create_recovery("fxctest", "55364", "0"))

