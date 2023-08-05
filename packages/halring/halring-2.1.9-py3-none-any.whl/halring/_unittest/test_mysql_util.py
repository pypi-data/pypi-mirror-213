# coding=utf-8
import unittest
from halring.mysql_lib.halring_mysql import MySqlUtil


class TestMySqlUtil(unittest.TestCase):
    """
    UnitTest
    Author: xqzhou
    """
    def test_mysql_util_001_db_connect_disconnect_ok_serv1(self):
        input_ip = "197.2.55.4"
        input_user = "root"
        input_pwd = "SseSql@dm1n"
        input_db = "mysql"
        mysql = MySqlUtil(input_ip, input_user, input_pwd, input_db)
        mysql.db_connect()
        mysql.db_disconnect()

    def test_mysql_util_002_db_connect_disconnect_ok_serv2(self):
        input_ip = "197.2.55.3"
        input_user = "root"
        input_pwd = "SseSql@dm1n"
        input_db = "mysql"
        mysql = MySqlUtil(input_ip, input_user, input_pwd, input_db)
        mysql.db_connect()
        mysql.db_disconnect()

    def test_mysql_util_003_db_connect_disconnect_ok_serv3(self):
        input_ip = "197.2.55.5"
        input_user = "root"
        input_pwd = "SseSql@dm1n"
        input_db = "mysql"
        mysql = MySqlUtil(input_ip, input_user, input_pwd, input_db)
        mysql.db_connect()
        mysql.db_disconnect()

    def test_mysql_util_004_db_connect_disconnect_ok_serv4(self):
        input_ip = "197.2.55.3"
        input_user = "aqcdb001"
        input_pwd = "Yg0ng@n6"
        input_db = "aqcdb_dev"
        mysql = MySqlUtil(input_ip, input_user, input_pwd, input_db)
        mysql.db_connect()
        result=mysql.execute_query("")
        print(result)
        mysql.db_disconnect()

    def test_mysql_util_005_db_backup(self):
        input_ip = "197.2.55.3"
        input_user = "root"
        input_pwd = "SseSql@dm1n"
        input_db = "flask_demo_db"
        mysql = MySqlUtil(input_ip, input_user, input_pwd, input_db)
        a=mysql.db_dump_all(input_db,"D:\\2020\\4.sql")
        print(a)

    def test_mysql_util_005_db_backup_struct(self):
        input_ip = "197.2.55.3"
        input_user = "root"
        input_pwd = "SseSql@dm1n"
        input_db = "flask_demo_db"
        mysql = MySqlUtil(input_ip, input_user, input_pwd, input_db)
        a=mysql.db_dump_struct(input_db,"D:\\2020\\5.sql")
        print(a)

    def test_mysql_util_005_db_recovery(self):
        input_ip = "197.2.55.3"
        input_user = "root"
        input_pwd = "SseSql@dm1n"
        input_db = "stest"
        mysql = MySqlUtil(input_ip, input_user, input_pwd, input_db)
        a = mysql.db_import(input_db, "D:\\2020\\53.sql")
        print(a)
