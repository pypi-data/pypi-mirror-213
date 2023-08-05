# coding=utf-8
from mysql_lib.halring_mysql import MySqlUtil
from halring.common.halring_common import CommonUtil
from halring.common.halring_string import StringUtil
from halring.common.halring_datetime import DatetimeUtil
from halring.common.halring_const_variable import ConstVariable
from loguru import logger


class DbAqcdbUtil(object):
    """
    database aqcdb 操作专用库
    1、取数据库表数据的功能为主
    aqcdb_ip = AQCDB数据库实例：INSTANCE_AQCDB_TEST_IP测试环境 和 INSTANCE_AQCDB_PROD_IP生产环境, aqcdb_instance = INSTANCE_AQCDB_DEV,INSTANCE_AQCDB_TEST,INSTANCE_AQCDB_PROD
    host_range = 查询测试机范围：指定范围格式为AST591|AST592，如不填写则为所有对AQCDB中HOST_INFO表中涉及主机均视为范围内
    """
    def __init__(self, aqcdb_ip, aqcdb_instance, host_range=""):
        self._aqcdb_ip   = aqcdb_ip
        self._aqcdb_user = "aqcdb001"
        self._aqcdb_pwd  = "Yg0ng@n6"
        self._aqcdb_db   = aqcdb_instance
        self._host_range_list = host_range.split("|")

    def put_host_range(self, new_host_range):
        """
        功能：重置初始化构建时的主机范围列表
        输入参数：new_host_range 新的主机范围
        返回值：无
        """
        self._host_range_list = new_host_range.split("|")

    def get_host_range(self):
        """
        功能：显示主机范围列表
        输入参数：无
        返回值：范围主机范围列表
        """
        return self._host_range_list

    def get_host_info_from_aqcdb(self):
        """
        功能：获取AQCDB中主机范围内HOST_INFO表内的主机名与IP的对应关系表
        输入参数：无
        返回值：<DICT>指定主机范围内主机名与IP对应表
        """
        host_info_dict = {}
        host_range_sql_where_range = StringUtil().string_conv_list_to_str(self._host_range_list, "'", "'", ", ")
        mysql = MySqlUtil(self._aqcdb_ip , self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select idkey, host_ip, host_type, host_status from host_info where idkey in (" + host_range_sql_where_range + ") order by host_type, idkey asc;"
        result = mysql.execute_query(sql)
        for item in result:
            host_name   = str(item[0])
            host_ip     = str(item[1])
            host_type   = str(item[2])
            host_status = str(item[3])
            host_info_dict[host_name] = host_ip + "|" + host_type + "|" + host_status
        mysql.db_disconnect()
        return host_info_dict

    def get_host_info_full_from_aqcdb(self):
        """
        功能：获取AQCDB中主机范围内HOST_INFO表内的主机名的全部信息
        输入参数：无
        返回值：<DICT>指定主机范围内主机名与IP对应表
        """
        host_info_dict = {}
        host_range_sql_where_range = StringUtil().string_conv_list_to_str(self._host_range_list, "'", "'", ", ")
        mysql = MySqlUtil(self._aqcdb_ip , self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select idkey, host_ip, host_type, host_description, project_info_idkey, project_module_name, host_owner, host_status, host_system, host_remark from host_info order by host_type, idkey asc;"
        result = mysql.execute_query(sql)
        for item in result:
            idkey = str(item[0])
            host_ip = str(item[1])
            host_type = str(item[2])
            host_description = str(item[3])
            project_info_idkey = str(item[4])
            project_module_name = str(item[5])
            host_owner = str(item[6])
            host_status = str(item[7])
            host_system = str(item[8])
            host_remark = str(item[9])
            host_info_dict[idkey] = host_ip + "|" + host_type + "|" + host_description + "|" \
                                    + project_info_idkey + "|" + project_module_name + "|" + host_owner + "|" \
                                    + host_status + "|" + host_system + "|" + host_remark
        mysql.db_disconnect()
        return host_info_dict

    def get_host_env_info_from_aqcdb(self, mode=""):
        """
        功能：获取AQCDB中主机范围内HOST_ENV_INFO表内的主机名上各账户对应分配用户的关系表
        输入参数：mode-默认为主机名分列成每个主机对账户，当输入MERGE时为原始的主机合并对应账户
        返回值：<DICT>指定主机范围内主机名上各账户对应分配用户的关系表
        """
        host_env_info_dict = {}
        host_range_sql_where_range = StringUtil().string_conv_list_to_str(self._host_range_list, "host_info_idkey like '%", "%'", " or ")

        # 获取HOST_INFO用于后续在HOST_ENV_INFO时补充主机对应IP的信息
        host_info_dict = self.get_host_info_from_aqcdb()

        # 获取HOST_ENV_INFO的信息
        mysql = MySqlUtil(self._aqcdb_ip , self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select host_info_idkey, host_env_user, host_env_pwd, host_env_type, host_env_owner, host_env_status, host_env_remark from host_env_info where " + host_range_sql_where_range + " order by host_info_idkey, host_env_user asc;"
        result = mysql.execute_query(sql)
        for item in result:
            host_info_idkey = str(item[0])
            host_env_user   = str(item[1])
            host_env_pwd    = str(item[2])
            host_env_type   = str(item[3])
            host_env_owner  = str(item[4])
            host_env_status = str(item[5])
            host_env_remark = str(item[6])
            if ConstVariable.MODE_MERGE in mode:
                host_info_dict_key = host_info_idkey + "|" + host_env_user
                host_info_dict_val = host_info_idkey + "|" + host_env_user + "|" + host_env_user.split("_")[-1] + "|" + host_env_type + "|" + host_env_owner + "|" + host_env_remark
                host_env_info_dict[host_info_dict_key] = host_info_dict_val
            else:
                for host_info_idkey_item in host_info_idkey.split(","):
                    if host_info_idkey_item in host_info_dict.keys():
                        host_info_dict_key = host_info_idkey_item + "|" + host_env_user
                        host_info_dict_val = host_info_idkey_item + "|" + host_info_dict[host_info_idkey_item] + "|" + host_env_user + "|" + host_env_pwd + "|" + host_env_user.split("_")[-1] + "|" + host_env_type + "|" + host_env_owner + "|" + host_env_status + "|" + host_env_remark
                        host_env_info_dict[host_info_dict_key] = host_info_dict_val
        mysql.db_disconnect()
        return host_env_info_dict


    def get_host_env_info_from_aqcdb_select_area(self, select_area=""):
        """
        功能：获取AQCDB中主机范围内HOST_ENV_INFO表内的主机名上各账户对应分配用户的关系表
        输入参数：select_area_list-指定范围
        返回值：<DICT>指定主机范围内主机名上各账户对应分配用户的关系表
        """
        host_env_info_dict = {}

        if select_area == "":
            host_range_sql_where_range = StringUtil().string_conv_list_to_str(self._host_range_list, "host_info_idkey like '%", "%'", " or ")
        else:
            select_area_list = select_area.split("|")
            host_range_sql_where_range = StringUtil().string_conv_list_to_str(select_area_list, "host_info_idkey like '%", "%'", " or ")

        # 获取HOST_ENV_INFO的信息
        mysql = MySqlUtil(self._aqcdb_ip , self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select host_info_idkey, host_env_user, host_env_type, host_env_description, host_env_owner, host_env_status, host_env_pwd, host_env_remark from host_env_info where " + host_range_sql_where_range + " order by host_info_idkey, host_env_user asc;"
        result = mysql.execute_query(sql)
        for item in result:
            host_info_idkey = str(item[0])
            host_env_user = str(item[1])
            host_env_type = str(item[2])
            host_env_description = str(item[3])
            host_env_owner = str(item[4])
            host_env_status = str(item[5])
            host_env_pwd = str(item[6])
            host_env_remark = str(item[7])
            host_info_dict_key = host_info_idkey + "|" + host_env_user
            host_info_dict_val = host_env_type + "|" + host_env_description + "|" + host_env_owner + "|" + host_env_status + "|" + host_env_pwd + "|" + host_env_remark
            host_env_info_dict[host_info_dict_key] = host_info_dict_val
        mysql.db_disconnect()
        return host_env_info_dict

    def get_host_user_owner_from_merge_host_env_info(self, merge_host_env_info_dict, host, user):
        """
        功能：获得，需要与get_host_env_info_from_aqcdb(MODE=MERGE)配套使用
        输入参数：merge_host_env_info_dict-合并模式下主机用户字典, host-待查主机, user-待查账户
        返回值：<STRING>返回查询到的主机对应所属者
        """
        rtn_onwer = ""
        host_prefix = host[0:4]
        for key_merge, val_merge in merge_host_env_info_dict.items():
            merge_host = val_merge.split("|")[0]
            host_user = val_merge.split("|")[1]
            host_env_owner = val_merge.split("|")[4]
            if host_prefix in merge_host and host_user == user:
                rtn_onwer = host_env_owner
            else:
                pass
        return rtn_onwer

    def get_host_env_info_by_host_env_type(self, host_env_type, mode=""):
        """
        功能：获取AQCDB中主机范围内HOST_ENV_INFO表内的主机名上各账户对应分配用户的关系表
        输入参数：<STRING>host_env_type 允许在调用函数时重置范围，默认为使用构建对象时的范围
                <STRING>mode          模式：默认空，输出所有；MODE_ONE_HOST，只输出些类机器的其中一台
        返回值：<DICT>指定主机范围内主机名上各账户对应分配用户的关系表
        """
        new_dict = {}
        host_env_info_dict = self.get_host_env_info_from_aqcdb()
        CommonUtil().show_dict(host_env_info_dict, "host_env_info_dict")
        prev_host_prefix = ""
        for key, val in host_env_info_dict.items():
            for host_env_type_item in host_env_type.split("|"):
                if "|" + host_env_type_item + "|" in val:
                    if ConstVariable.MODE_ONE_HOST in mode:
                        curr_host_prefix = key[0:4]
                        if prev_host_prefix == curr_host_prefix:
                            pass
                        else:
                            key_host = key.split("|")[0]
                            new_dict[key_host] = val
                            prev_host_prefix = curr_host_prefix
                    else:
                        new_dict[key] = val
                else:
                    pass
        return new_dict

    def get_host_env_dict_from_aqcdb(self):
        """
        功能：获取AQCDB中主机范围内HOST_ENV_INFO表内的主机与主机上的分配环境的对应关系
        输入参数：无
        返回值：<DICT>指定主机范围内主机与主机上的分配账户对应关系
        """
        host_env_dict = {}
        host_range_sql_where_range = StringUtil().string_conv_list_to_str(self._host_range_list, "host_info_idkey like '%", "'", " or ")

        # 获取HOST_INFO用于后续在HOST_ENV_INFO时补充主机对应IP的信息
        host_info_dict = self.get_host_info_from_aqcdb()

        # 获取HOST_ENV_INFO的信息
        mysql = MySqlUtil(self._aqcdb_ip , self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select host_info_idkey, host_env_user from host_env_info where " + host_range_sql_where_range + " order by host_info_idkey, host_env_user asc;"
        result = mysql.execute_query(sql)
        for item in result:
            host_info_idkey = str(item[0]).replace(",","|")
            host_env_no     = str(item[1]).split("_")[1]
            if host_info_idkey in host_env_dict.keys():
                host_env_dict[host_info_idkey] = host_env_dict[host_info_idkey] + "|" + host_env_no
            else:
                host_env_dict[host_info_idkey] = host_env_no
        mysql.db_disconnect()
        return host_env_dict

    def execute_sql_in_aqcdb(self, sql_list):
        """
        功能：向AQCDB中执行SQL语句
        输入参数：<LIST>sql_list SQL命令列表
        返回值：无
        """
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        for sql_item in sql_list:
            mysql.execute_sql(sql_item)
        mysql.db_disconnect()

    def get_host_resource_info_from_aqcdb_by_type(self, input_type):
        """
        功能：获取AQCDB中主机范围内HOST_RESOURCE_INFO表内的主机名上各磁盘卷的配置信息关系表
        输入参数：<STRING>TYPE 资源类型，DISK为磁盘，MEM为内存
        返回值：<DICT>指定主机范围内主机名各磁盘卷的配置信息表，KEY<STRING>为主机，VAL<DICT>为该主机上各磁盘卷对应配置的字典
        """
        # 主机资源信息表多重字典，最终给出：KEY=HOST|TYPE VAL=LABAL=THREASHOLD
        host_resource_dict = {}
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select host_info_idkey, host_resource_type, host_resource_label, host_resource_label_desc, host_resource_total, host_resource_total_warn_threshold, host_resource_total_error_threshold, user_resource_warn_threshold, user_resource_error_threshold from host_resource_info where host_resource_type = '" + input_type + "' order by host_info_idkey asc"
        result = mysql.execute_query(sql)
        for item in result:
            host_info_idkey = str(item[0])
            host_resource_type = str(item[1])
            host_resource_label = str(item[2])
            host_resource_label_desc = str(item[3])
            host_resource_total = str(item[4])
            host_resource_total_warn_threshold = str(item[5])
            host_resource_total_error_threshold = str(item[6])
            user_resource_warn_threshold = str(item[7])
            user_resource_error_threshold = str(item[8])
            for host_info_idkey_item in host_info_idkey.split(","):
                host_resource_dict_key = host_info_idkey_item + "|" + host_resource_type
                if host_resource_dict_key in host_resource_dict.keys():
                    host_resource_dict_val_dict = host_resource_dict[host_resource_dict_key]
                    host_resource_dict_val_dict[host_resource_label] = host_resource_total + "|" + host_resource_total_warn_threshold + "|" + host_resource_total_error_threshold + "|" + user_resource_warn_threshold + "|" + user_resource_error_threshold
                else:
                    host_resource_dict_val_dict = {}
                    host_resource_dict_val_dict[host_resource_label] = host_resource_total + "|" + host_resource_total_warn_threshold + "|" + host_resource_total_error_threshold + "|" + user_resource_warn_threshold + "|" + user_resource_error_threshold
                host_resource_dict_val = host_resource_dict_val_dict
                host_resource_dict[host_resource_dict_key] = host_resource_dict_val
        mysql.db_disconnect()
        return host_resource_dict

    def get_host_resource_info_used_threshold_from_aqcdb_by_type(self, input_type):
        """
        功能：获取主机的内存及磁盘的各项阀值的字典
        输入参数：<STRING>TYPE 资源类型，DISK为磁盘，MEM为内存
        返回值：<DICT>主机的内存及磁盘的各项阀值的字典 KEY=HOST|TYPE|DSECorDIR = TOTAL_WARN_TH|TOTAL_ERR_TH|USER_WARN_TH|USER_ERR_TH|
        """
        host_resource_dict = {}
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select host_info_idkey,host_resource_type,host_resource_label,host_resource_total,host_resource_total_warn_threshold,host_resource_total_error_threshold,user_resource_warn_threshold,user_resource_error_threshold from host_resource_info where host_resource_type = '" + input_type + "' order by host_info_idkey asc"
        result = mysql.execute_query(sql)
        for item in result:
            host_list = str(item[0])
            resource_type = str(item[1])
            resource_label = str(item[2])
            host_resource_total = str(item[3])
            total_warn_threshold = str(item[4])
            total_error_threshold = str(item[5])
            user_warn_threshold = str(item[6])
            user_error_threshold = str(item[7])
            val_host_res_dict = host_resource_total + "|" + total_warn_threshold + "|" + total_error_threshold + "|" + user_warn_threshold + "|" + user_error_threshold
            for host in host_list.split(","):
                key_host_res_dict = host + "|" + resource_type + "|" + resource_label
                host_resource_dict[key_host_res_dict] = val_host_res_dict
        mysql.db_disconnect()
        return host_resource_dict

    def get_hostgroup_from_host_resource_info_by_type(self, input_type):
        """
        功能：通过主机名，在HOST_RESOURCE_INFO中找到主机名对应主机组群的字典
        输入参数：input_type = MEM, 直接输出，DISK，需要转换
        返回值：<DICT>主机对应主机集群字典，KEY=host VAL=hostgroup
        """
        host_resource_dict = {}
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select host_info_idkey from host_resource_info where host_resource_type = '" + input_type + "' order by host_info_idkey asc"
        result = mysql.execute_query(sql)
        for item in result:
            host = str(item[0])
            if input_type is ConstVariable.RESOURCE_TYPE_MEM:
                host_resource_dict[host] = host
            elif input_type is ConstVariable.RESOURCE_TYPE_DISK:
                for host_item in host.split(","):
                    host_resource_dict[host_item] = host
            else:
                logger.error("input_type {0} error".format(input_type))
                assert 0
        mysql.db_disconnect()
        return host_resource_dict


    def get_last_snapshot_from_host_usermem_mon(self):
        """
        功能：获取host_usermem_mon表中按gmt_create的最后一幅时间戳的记录
        输入参数：无
        返回值：last_gmt_datetime最后一幅的时间戳，last_snapshot_mem_dict最后一幅的内容
        """
        dtu = DatetimeUtil()
        curr_datetime = dtu.get_format_curr_datetime(ConstVariable.FORMAT_DATETIME_MYSQL)
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()

        drift_second = 0
        drift_second_interval = 600
        result = ()
        last_snapshot_mem_dict = {}
        host_range_sql_where_range = StringUtil().string_conv_list_to_str(self._host_range_list, "'", "'", ", ")
        while len(result) == 0:
            drift_second = drift_second + drift_second_interval
            search_datetime = dtu.drift_datetime_mysql(ConstVariable.FORMAT_DATETIME_MYSQL, curr_datetime, ConstVariable.DRIFT_DIRECTION_FORWARD, drift_second)
            sql = "select gmt_create, gmt_modified, host_info_idkey, host_env_user, resource_type, resource_label, resource_user_used, remark from host_usermem_mon where gmt_create > '" + search_datetime + "' and host_info_idkey in (" + host_range_sql_where_range + ")"
            result = mysql.execute_query(sql)
        else:
            for item in result:
                logger.debug("item = {0}".format(item))
                last_gmt_datetime = str(item[0])
                host = str(item[2])
                user = str(item[3])
                type = str(item[4])
                label = str(item[5])
                user_used = str(item[6])
                user_mark = str(item[7])
                key_dict = host + "|" + user + "|" + type + "|" + label
                val_dict = user_used + "|" + user_mark
                if user_used == ConstVariable.RSLT_USED_INIT:
                    continue
                last_snapshot_mem_dict[key_dict] = val_dict
        return last_gmt_datetime, last_snapshot_mem_dict

    def get_last_snapshot_from_host_mem_mon(self):
        """
        功能：获取host_mem_mon表中按gmt_create的最后一幅时间戳的记录
        输入参数：无
        返回值：last_gmt_datetime最后一幅的时间戳，last_snapshot_mem_dict最后一幅的内容
        """

        dtu = DatetimeUtil()
        curr_datetime = dtu.get_format_curr_datetime(ConstVariable.FORMAT_DATETIME_MYSQL)
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()

        drift_second = 0
        drift_second_interval = 600
        result = ()
        last_snapshot_mem_dict = {}
        host_range_sql_where_range = StringUtil().string_conv_list_to_str(self._host_range_list, "'", "'", ", ")
        while len(result) == 0:
            drift_second = drift_second + drift_second_interval
            search_datetime = dtu.drift_datetime_mysql(ConstVariable.FORMAT_DATETIME_MYSQL, curr_datetime, ConstVariable.DRIFT_DIRECTION_FORWARD, drift_second)
            sql = "select gmt_create, gmt_modified, host_info_idkey, free_mem, free_cpu, online_env, remark from host_mem_mon where gmt_create > '" + search_datetime + "' and host_info_idkey in (" + host_range_sql_where_range + ")"
            result = mysql.execute_query(sql)
        else:
            for item in result:
                logger.debug("item = {0}".format(item))
                last_gmt_datetime = str(item[0])
                host = str(item[2])
                free_mem = str(item[3])
                free_cpu = str(item[4])
                online_env_list_str = str(item[5])
                remark = str(item[6])
                last_snapshot_mem_dict[host] = free_mem + "|" + free_cpu + "|" + online_env_list_str + "|" + remark
        return last_gmt_datetime, last_snapshot_mem_dict

    def get_last_snapshot_from_host_userdisk_mon(self):
        """
        功能：获取host_userdisk_mon表中按gmt_create的最后一幅时间戳的记录
        输入参数：无
        返回值：last_gmt_datetime, last_snapshot_disk_dict
        """
        dtu = DatetimeUtil()
        curr_datetime = dtu.get_format_curr_datetime(ConstVariable.FORMAT_DATETIME_MYSQL)
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()

        drift_second = 0
        drift_second_interval = 600
        result = ()
        last_snapshot_disk_dict = {}
        host_range_sql_where_range = StringUtil().string_conv_list_to_str(self._host_range_list, "'", "'", ", ")
        while len(result) == 0:
            drift_second = drift_second + drift_second_interval
            search_datetime = dtu.drift_datetime_mysql(ConstVariable.FORMAT_DATETIME_MYSQL, curr_datetime, ConstVariable.DRIFT_DIRECTION_FORWARD, drift_second)
            sql = "select gmt_create, gmt_modified, host_info_idkey, host_env_user, resource_type, resource_label, resource_label_sub, resource_user_used, remark from host_userdisk_mon where gmt_create > '" + search_datetime + "' and host_info_idkey in (" + host_range_sql_where_range + ")"
            result = mysql.execute_query(sql)
        else:
            for item in result:
                logger.debug("item = {0}".format(item))
                last_gmt_datetime = str(item[0])
                host = str(item[2])
                user = str(item[3])
                type = str(item[4])
                label = str(item[5])
                label_sub = str(item[6])
                user_used = str(item[7])
                user_mark = str(item[8])
                key_dict = host + "|" + user + "|" + type + "|" + label + "|" + label_sub
                val_dict = user_used
                if user_mark == ConstVariable.RSLT_CHECK_FAIL:
                    continue
                last_snapshot_disk_dict[key_dict] = val_dict
        return last_gmt_datetime, last_snapshot_disk_dict

    def get_last_snapshot_from_host_disk_mon(self):
        """
        功能：获取host_disk_mon表中按gmt_create的最后一幅时间戳的记录
        输入参数：无
        返回值：last_gmt_datetime, last_snapshot_disk_dict
        """
        dtu = DatetimeUtil()
        curr_datetime = dtu.get_format_curr_datetime(ConstVariable.FORMAT_DATETIME_MYSQL)
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()

        drift_second = 0
        drift_second_interval = 600
        result = ()
        last_snapshot_disk_dict = {}
        host_range_sql_where_range = StringUtil().string_conv_list_to_str(self._host_range_list, "'", "'", ", ")
        while len(result) == 0:
            drift_second = drift_second + drift_second_interval
            search_datetime = dtu.drift_datetime_mysql(ConstVariable.FORMAT_DATETIME_MYSQL, curr_datetime, ConstVariable.DRIFT_DIRECTION_FORWARD, drift_second)
            sql = "select gmt_create, gmt_modified, host_info_idkey, disk_name, free_disk, remark from host_disk_mon where gmt_create > '" + search_datetime + "' and host_info_idkey in (" + host_range_sql_where_range + ")"
            result = mysql.execute_query(sql)
        else:
            for item in result:
                logger.debug("item = {0}".format(item))
                last_gmt_datetime = str(item[0])
                host = str(item[2])
                disk_name = str(item[3])
                free_disk = str(item[4])
                remark = str(item[5])
                key_dict = host + "|" + disk_name
                last_snapshot_disk_dict[key_dict] = free_disk + "|" + remark
        return last_gmt_datetime, last_snapshot_disk_dict

    def get_project_id_from_project_info(self):
        """
        功能：从project_info项目表获取项目ID列表
        输入参数：无
        返回值：<LIST>项目ID列表
        """
        project_id_list = []
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select idkey from project_info;"
        result = mysql.execute_query(sql)
        for item in result:
            project_id = str(item[0])
            project_id_list.append(project_id)
        mysql.db_disconnect()
        return project_id_list

    def get_user_from_user_info(self):
        """
        功能：从user_info项目表获取所有用户信息
        输入参数：无
        返回值：<DICT>用户列表
        """
        user_dict = {}
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select user_domain_idkey, user_domain_cnname, user_domain_userkey, remark from user_info;"
        result = mysql.execute_query(sql)
        for item in result:
            user_domain_idkey   = str(item[0])
            user_domain_cnname  = str(item[1])
            user_domain_userkey = str(item[2])
            remark = str(item[3])
            user_key = user_domain_idkey
            user_val = user_domain_cnname + "|" + user_domain_userkey + "|" + remark
            user_dict[user_key] = user_val
        mysql.db_disconnect()
        return user_dict

    def get_deploy_host_env_by_project(self, project):
        """
        根据项目获取可用于自动部署的主机及环境信息
        :param project: 项目名
        :return: <LIST>项目可用于部署的主机、ip、环境信息
        """
        deploy_host_env_list = []
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select idkey, host_ip from host_info where project_info_idkey like '%" + project + "%' and host_type like '%AUTODEPLOY%' and host_status = 'ON';"
        result = mysql.execute_query(sql)
        for item in result:
            host_name = item[0]
            host_ip = item[1]
            sql_env = "select host_env_user, host_env_pwd, host_env_owner from host_env_info where host_info_idkey like '%" + host_name + "%' and host_env_type = 'AQCTEST' and host_env_status = 'NORMAL'"
            result_env = mysql.execute_query(sql_env)
            for item_env in result_env:
                host_env_temp = host_name + "|" + host_ip + "|" + item_env[0] + "|" + item_env[1] + "|" + item_env[2]
                deploy_host_env_list.append(host_env_temp)
        mysql.db_disconnect()
        return deploy_host_env_list

    def select_table_where_data_from_table(self, select_value, table_value, where_value):
        """
        根据项目获取可用于自动部署的主机及环境信息
        :param project: 项目名
        :return: <TUPLE>项目可用于部署的主机、ip、环境信息
        """
        user_dict = {}
        mysql = MySqlUtil(self._aqcdb_ip, self._aqcdb_user, self._aqcdb_pwd, self._aqcdb_db)
        mysql.db_connect()
        sql = "select {0} from {1} where {2};".format(select_value, table_value, where_value)
        result = mysql.execute_query(sql)
        return result