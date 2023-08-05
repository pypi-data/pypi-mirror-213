# coding=utf-8
import pymysql
import os
from loguru import logger
import subprocess


class MySqlUtil:
    """
    MySQL Server
    Author: xqzhou
    """
    _connection = None

    def __init__(self, host, user, password, db, port=3306):
        """
        Init sql server.
        :param server:
            sql server ip address.
        :param user:
            username to login database.
        :param password:
            password to login database.
        :param db:
            database name.
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self._encode_type = ""

    def db_connect(self):
        """
        Connect to sql server data base.
        :return:
        """
        self._connection = pymysql.connect(host=self.host,
                                           port=self.port,
                                           user=self.user,
                                           password=self.password,
                                           database=self.db,
                                           charset='utf8')

        # log info
        if not self._connection:
            raise(NameError, "Failed to connect to my sql: {0}".format(self.host))
        else:
            logger.debug("Connect to My SQL: {0} user: {1} password: {2} db: {3}".format(self.host, self.user, self.password, self.db))

    def execute_query(self, query_sql):
        """
        Execute query sql statement.
        :param query_sql:
            query sql statement.
            example: "SELECT TOP 3 <column name> from <table name>"
        :return:
            list: fetched rows by @query_sql, each element is a meta group.
        """
        if self._connection:
            logger.debug("Execute query sql: {0}".format(query_sql))
        else:
            logger.error("No db connection for query: {0}".format(query_sql))
            return

        cur = self._connection.cursor()
        cur.execute(query_sql)
        rows = cur.fetchall()
        cur.close()

        str_query_rst = "  "
        for row in rows:
            str_query_rst += str(row) + "\n  "

        logger.debug("sql query result: {0}".format(str_query_rst))

        return rows

    def execute_sql(self, sql_statement):
        """
        Execute non-query sql statement.
        For example, INSERT, DELETE, DROP ...
        :param sql_statement:
            SQL statement.
            for example: "INSERT INTO <table name>(<column1, column2>) VALUES (value1, value2)"
        :return:
        """
        if self._connection:
            logger.info("Execute sql: {0}".format(sql_statement))
        else:
            logger.error("No db connection for sql: {0}".format(sql_statement))
            return

        cur = self._connection.cursor()
        try:
            cur.execute(sql_statement)
            self._connection.commit()
        except:
            self._connection.rollback()
            logger.error("Execute sql error")
            raise

    def db_disconnect(self):
        """
        Disconnected from sql server.
        :return:
        """
        if self._connection:
            logger.info("Disconnect from SQL Server: {0}".format(self.host))
            try:
                self._connection.close()
            except Exception as e:
                if "Already closed" in e:
                    pass
                else:
                    raise e

    @staticmethod
    def exec_shell(shell_script):
        proc = subprocess.Popen(shell_script, stdout=subprocess.PIPE, shell=True)
        res = proc.communicate()
        echo_str = res[0].decode().lstrip().rstrip()
        return_code = proc.returncode
        return {"echo_str": echo_str, "return_code": return_code, "str_return_code": str(return_code)}

    def db_dump_all(self, db_name, local_ini_path, outfile, platform='windows'):
        """
        导出指定数据库的结构及数据
        :param db_name:数据库名字
        :param outfile:输出dump文件.sql
        :return:{"status":True/False,
                "value":print}
        """
        # 需要执行的机器上有mysqldump的命令

        # local_ini_path = "temp_config_mysqldump.ini"

        print("Dump mysql:{0}".format(self.host))
        with open(local_ini_path, "w") as f:
            f.writelines("[mysqldump]\n")
            f.writelines("host={0}\n".format(self.host))
            f.writelines("port={0}\n".format(self.port))
            f.writelines("user={0}\n".format(self.user))
            f.writelines("password={0}\n".format(self.password))
        command = "mysqldump --defaults-extra-file={0} {1} > {2}".format(local_ini_path,db_name,outfile)
        print(command)
        if platform.lower() == 'windows':
            from halring.windows.halring_os import OsUtil
            self._osutil = OsUtil()
            self._encode_type = self._osutil.get_cmd_encode_type()
            result = self._osutil.popen_block2(command).get("message").decode(self._encode_type)
        else:
            result = self.exec_shell(command)['str_return_code']

        if result:
            result_status = False
            print(result)
        else:
            result_status = True
        result_dict = {
            "status": result_status,
            "value": result
        }
        os.remove(local_ini_path)
        return result_dict

    def db_dump_struct(self, db_name, local_ini_path, outfile, platform='windows'):
        """
        导出指定数据库的结构
        :param db_name:数据库名字
        :param local_ini_path 本地 ini 文件
        :param outfile:输出dump文件.sql
        :return:{"status":True/False,
                "value":print}
        """
        # 需要执行的机器上有mysqldump的命令

        # local_ini_path = "temp_config_mysqldump.ini"

        print("Dump mysql:{0}".format(self.host))
        with open(local_ini_path, "w") as f:
            f.writelines("[mysqldump]\n")
            f.writelines("host={0}\n".format(self.host))
            f.writelines("port={0}\n".format(self.port))
            f.writelines("user={0}\n".format(self.user))
            f.writelines("password={0}\n".format(self.password))
        command = "mysqldump --defaults-extra-file={0} --opt -d {1} > {2}".format(local_ini_path,db_name,outfile)
        print(command)
        if platform.lower() == 'windows':
            from halring.windows.halring_os import OsUtil
            self._osutil = OsUtil()
            self._encode_type = self._osutil.get_cmd_encode_type()
            result = self._osutil.popen_block2(command).get("message").decode(self._encode_type)
        else:
            result = self.exec_shell(command)['str_return_code']
        print(result)
        if result:
            result_status = False
            print(result)
        else:
            result_status = True
        result_dict = {
            "status": result_status,
            "value": result
        }
        os.remove(local_ini_path)

        return result_dict

    def db_import(self, db_name, in_file):
        """ 数据库导入
        :param db_name: 数据库名称
        :param in_file: 导入文件名次
        :return: 导入结果
        """
        # 需要执行的机器上有mysql的命令

        local_ini_path = "temp_config_mysql.ini"

        print("Recovery mysql:{0}".format(self.host))
        with open(local_ini_path, "w") as f:
            f.writelines("[client]\n")
            f.writelines("host={0}\n".format(self.host))
            f.writelines("port={0}\n".format(self.port))
            f.writelines("user={0}\n".format(self.user))
            f.writelines("password={0}\n".format(self.password))
        command = "mysql --defaults-extra-file={0} {1} < {2}".format(local_ini_path, db_name, in_file)
        print(command)
        from halring.windows.halring_os import OsUtil
        self._osutil = OsUtil()
        result = self._osutil.popen_block2(command).get("message").decode(self._encode_type)
        if result:
            result_status = False
            print(result)
        else:
            result_status = True
        result_dict = {
            "status": result_status,
            "value": result
        }
        os.remove(local_ini_path)
        return result_dict

