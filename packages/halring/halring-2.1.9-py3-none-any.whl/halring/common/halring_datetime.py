# coding=utf-8
import time
from loguru import logger
from .halring_const_variable import ConstVariable


class DatetimeUtil(object):
    """
    DateTimeUtil
    Author: xqzhou
    """
    def __init__(self):
        pass

    def get_format_curr_datetime(self, format_string):
        """
        功能：根据指定datetime格式返回当前日期时间
        输入参数：FORMAT_DATETIME_NORMAL = "%Y%m%d-%H:%M:%S"
                FORMAT_DATETIME_MYSQL  = "%Y-%m-%d %H:%M:%S"
        返回值：<STRING>指定日期格式的当前时间
        """
        ct = time.time()
        local_time = time.localtime(ct)
        rtn_recordtimestamp = time.strftime(format_string, local_time)
        #        logger.info("rtn_recordtimestamp: {0}".format(rtn_recordtimestamp))
        return rtn_recordtimestamp

    def calc_datetime(self, select_date):
        """
        功能：返回计算指定日期+当前时间，格式为20070312-08:50:04.000
        输入参数：
        返回值：<STRING>修改过日期时间+当前时间
        """
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = select_date + time.strftime("-%H:%M:%S", local_time)
        data_milesecs = (ct - int(ct)) * 1000
        rtn_recordtimestamp = "%s.%.03d" % (data_head, data_milesecs)
#        logger.info("rtn_recordtimestamp: {0}".format(rtn_recordtimestamp))
        return rtn_recordtimestamp

    def conv_datetime_to_timestamp(self, orgi_datetime, orgi_format_string=ConstVariable.FORMAT_DATETIME_MYSQL):
        """
        功能：格式转换根据时间格式转换指定格式时间字符串为时间戳（1970年开始的秒数）
        输入参数：orgi_format_string-YYYY-MM-DD HH:MM:SS orgi_datetime-需要转换的时间
        返回值：<INT>转换后的时间戳
        """
        orgi_datetime_array = time.strptime(orgi_datetime, orgi_format_string)
        new_time_stamp = int(time.mktime(orgi_datetime_array))
        return new_time_stamp

    def conv_timestamp_to_datetime(self, orgi_timestamp, new_format_string=ConstVariable.FORMAT_DATETIME_MYSQL):
        """
        功能：格式转换根据时间格式转换指定时间戳（1970年开始的秒数）为时间字符串
        输入参数：orgi_timestamp-需要转换的时间戳 new_format_string-YYYY-MM-DD HH:MM:SS
        返回值：<STRING>转换后的日期时间YYYY-MM-DD HH:MM:SS
        """
        new_datetime_array = time.localtime(orgi_timestamp)
        new_datetime = time.strftime(new_format_string, new_datetime_array)
        return new_datetime

    def drift_datetime_mysql(self, format_string, datetime, drift_direction, drift_second):
        """
        功能：指定时间向前或向后方面进行漂移
        输入参数：format_string-MYSQL格式时间YYYY-MM-DD HH:MM:SS datetime-"2020-10-12 14:19:31"，drift_direction-漂移方向：FORWARD向前，BACKWARD向后，drift_second-漂移秒数
        返回值：<STRING>漂移后的日期时间
        """
        orgi_timestamp = self.conv_datetime_to_timestamp(datetime, format_string)
        if ConstVariable.DRIFT_DIRECTION_FORWARD in drift_direction:
            new_timestamp = orgi_timestamp - drift_second
        elif ConstVariable.DRIFT_DIRECTION_BACKWARD in drift_direction:
            new_timestamp = orgi_timestamp + drift_second
        else:
            logger.error("drift direction error {0}".format(drift_direction))
            assert 0
        new_datetime = self.conv_timestamp_to_datetime(new_timestamp, format_string)
        return new_datetime