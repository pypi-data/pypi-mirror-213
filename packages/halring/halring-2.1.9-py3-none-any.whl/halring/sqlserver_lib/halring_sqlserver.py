# coding=utf-8
from loguru import logger
import pymssql


class SqlServerUtil(object):
    """
    MS SQL Server
    Author: xqzhou
    """
    _connection = None

    def __init__(self, host, port, user, password, db):
        """
        Init sql server.
        Author: xqzhou
        :param server:
            sql server ip address.
        :param user:
            username to login database.
        :param password:
            password to login database.
        :param db:
            database name.
        """
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._db = db

    def db_connect(self):
        """
        Connect to sql server data base.
        :return:
        """
        self._connection = pymssql.connect(host=self._host,
                                           port=self._port,
                                           user=self._user,
                                           password=self._password,
                                           database=self._db,
                                           charset='utf8')

        # log info
        if not self._connection:
            raise(NameError, "Failed to connect to mssql: {0}".format(self._host))
        else:
            logger.debug("Connect to mssql: {0} user: {1} password: {2} db: {3}".format(self._host, self._user, self._password, self._db))

    def query_sql(self, query_sql):
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
            logger.info("Execute sql success")
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
            logger.info("Disconnect from SQL Server: {0}".format(self._host))
            try:
                self._connection.close()
            except Exception as e:
                if "Already closed" in e:
                    pass
                else:
                    raise e


if __name__ == '__main__':
    pass