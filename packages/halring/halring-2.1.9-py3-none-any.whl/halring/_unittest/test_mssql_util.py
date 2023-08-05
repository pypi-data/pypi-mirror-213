# coding=utf-8
import unittest
from halring.sqlserver_lib.halring_sqlserver import SqlServerUtil as MsSqlUtil


class TestMySqlUtil(unittest.TestCase):
    """
    UnitTest
    Author: xqzhou
    """
    def test_mysql_util_001_db_connect_disconnect_ok_serv1(self):
        input_ip = "197.2.55.3"
        input_port = "1433"
        input_user = "sa"
        input_pwd = "SseSql@dm1n"
        input_db = "master"
        mssql = MsSqlUtil(input_ip, input_port, input_user, input_pwd, input_db)
        mssql.db_connect()
        mssql.db_disconnect()

    def test_mysql_util_002_db_connect_disconnect_ok_serv2(self):
        input_ip = "197.2.55.4"
        input_port = "1433"
        input_user = "sa"
        input_pwd = "SseSql@dm1n"
        input_db = "master"
        mssql = MsSqlUtil(input_ip, input_port, input_user, input_pwd, input_db)
        mssql.db_connect()
        mssql.db_disconnect()
