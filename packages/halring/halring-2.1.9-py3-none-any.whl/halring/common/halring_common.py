# coding=utf-8
import re

from loguru import logger
from .halring_const_variable import ConstVariable


class CommonUtil(object):
    """
    common_util: assemble common functions
    Author: xqzhou
    """

    def __init__(self):
        pass

    def show_list(self, input_list, input_list_name):
        rtn = 0
        logger.info("[SHOWTITLE]{0}".format(input_list_name))
        if isinstance(input_list, list):
            for item in input_list:
                logger.info("[SHOW]{0}".format(item))
            logger.info("[SHOWCNT]{0}".format(len(input_list)))
            rtn = 1
        else:
            logger.error("[SHOWERR]{0} TYPE ERR {1}".format(input_list_name, type(input_list)))
            rtn = 0
        return rtn

    def show_dict(self, input_dict, input_dict_name):
        rtn = 0
        logger.info("[SHOWTITLE]{0}".format(input_dict_name))
        if isinstance(input_dict, dict):
            for key, val in input_dict.items():
                if isinstance(val, list):
                    logger.info("[SHOW]{0}".format(key))
                    for val_item in val:
                        logger.info("[SHOWSUB]{0}".format(val_item))
                if isinstance(val, dict):
                    logger.info("[SHOW_KEY]{0}".format(key))
                    for key, val in val.items():
                        logger.info("[SHOWSUB_VAL]{0}={1}".format(key, val))
                else:
                    logger.info("[SHOW]{0}={1}".format(key, val))
            logger.info("[SHOWCNT]{0}".format(len(input_dict)))
            rtn = 1
        else:
            logger.error("[SHOWERR]{0} TYPE ERROR {1}".format(input_dict_name, type(input_dict)))
            rtn = 0
        return rtn

    def show_str(self, input_str, input_str_name):
        rtn = 0
        logger.info("[SHOWTITLE]{0}".format(input_str_name))
        if isinstance(input_str, str):
            logger.info("[SHOW]{0}".format(input_str))
            logger.info("[SHOWCNT]{0}".format(len(input_str)))
            rtn = 1
        else:
            logger.error("[SHOWERR]{0} TYPE ERR {1}".format(input_str_name, type(input_str)))
            rtn = 0
        return rtn

    def find_user_from_host_disk_dir(self, host, disk_dir):
        logger.debug("host={0} disk_dir={1}".format(host, disk_dir))
        if re.search(r'^000000$', disk_dir):
            disk_user = "目录空间总计"
        elif re.search(r'^TOFF[0-9][0-9]$', disk_dir):
            if "ES" in host:
                disk_user = "NOP_" + disk_dir.split("TOFF")[1]
            else:
                disk_user = "NGTS_" + disk_dir.split("TOFF")[1]
        elif re.search(r'^[0-9][0-9]$', disk_dir):
            if "ES" in host:
                disk_user = "NOP_" + disk_dir
            else:
                disk_user = "NGTS_" + disk_dir
        else:
            disk_user = ConstVariable.NO_DISTINGUISH_USER
        return disk_user

    def conv_size(self, old_size, old_size_type, new_size_type=""):
        """
        功能：大小单位转换，先将原值转为单位B，然后根据要求转新为新的单位
        输入：old_size-原始大小，old_size_type-原始数值类型，new_size_type-新转换后的类型
        返回：<STRING>转换后的单位值
        """
        # 输入数据还原来为B为单位
        if ConstVariable.CONV_SIZE_KB in old_size_type or ConstVariable.CONV_SIZE_KB in old_size:
            tmp_size = int(float(old_size.split("KB")[0]) * 1024)
        elif ConstVariable.CONV_SIZE_MB in old_size_type or ConstVariable.CONV_SIZE_MB in old_size:
            tmp_size = int(float(old_size.split("MB")[0]) * 1024 * 1024)
        elif ConstVariable.CONV_SIZE_GB in old_size_type or ConstVariable.CONV_SIZE_GB in old_size:
            tmp_size = int(float(old_size.split("GB")[0]) * 1024 * 1024 * 1024)
        else:
            tmp_size = int(float(old_size))
        # 输出数据根据要求的类型转换单位
        if ConstVariable.CONV_SIZE_KB in new_size_type:
            new_size = str(int(tmp_size / 1024))
        elif ConstVariable.CONV_SIZE_MB in new_size_type:
            new_size = str(int(tmp_size / 1024 / 1024))
        elif ConstVariable.CONV_SIZE_GB in new_size_type:
            new_size = str(int(tmp_size / 1024 / 1024 / 1024))
        else:
            new_size = str(tmp_size)
        return new_size

    def conv_envno_to_user(self, envno, host):
        """
        功能：转换环境号至用户，除了ES系列，是环境号=》NOP_环境号，其它都是环境号=》NGTS_环境号
        输入：envno-环境号, host-主机名
        返回：<STRING>envno_user-转换后的环境号对应账户
        """
        if "ES" in host:
            envno_user = "NOP_" + envno
        elif "CS" in host:
            envno_user = "NOP_" + envno
        else:
            envno_user = "NGTS_" + envno
        return envno_user

    def check_item_from_ignore_dir_tuple(self, check_item):
        """
        功能：检查指定字段是否在ConstVariable.IGNORE_DIR_TUPLE范围内
        输入：待检查字段
        返回：<BOOL>True检查到 ,False未检查到
        """
        rtn_search = ""
        key_search = ""
        if ConstVariable.DIR_NODENUM in check_item:
            key_search = ConstVariable.DIR_NODENUM
        else:
            key_search = check_item

        if key_search in ConstVariable.IGNORE_DIR_TUPLE:
            rtn_search = True
        else:
            rtn_search = False
        return rtn_search

    def conv_str_to_list(self, input_str, input_deli):
        """
        功能：指定字段串，以指定符号分割后，转换为数据
        输入：input_str-输入字符串, input_deli-字符串分割符
        返回：<LIST>rtn_list-转换成数组
        """
        rtn_list = []
        if isinstance(input_str, str):
            logger.info("[SHOW]{0}".format(input_str))
            logger.info("[SHOWCNT]{0}".format(len(input_str)))
            rtn_list = input_str.split(input_deli)
        else:
            logger.error("[SHOWERR]TYPE ERR {0}".format(type(input_str)))
        return rtn_list

    def conv_list_to_2dlist(self, input_list, input_deli):
        """
        功能：指定字段串，以指定符号分割后，转换为数据
        输入：input_str-输入字符串, input_deli-字符串分割符
        返回：<LIST>rtn_2dlist-转换成数组
        """
        rtn_2dlist = []
        if isinstance(input_list, list):
            for item in input_list:
                logger.info("[SHOW]{0}".format(item))
                item_list = item.split(input_deli)
                rtn_2dlist.append(item_list)
        else:
            logger.error("[SHOWERR]TYPE ERR {0}".format(type(input_list)))
        return rtn_2dlist


if __name__ == '__main__':
    test_list = [1, 2, 3, 4, 5, 6]
    test_dict = {'A': '1', 'B': '2', 'C': '3'}
    test_str = "123456"
    CommonUtil().show_list(test_list, "SHOW_LIST")
    CommonUtil().show_dict(test_dict, "SHOW_DICT")
    CommonUtil().show_str(test_str, "SHOW_STRING")
