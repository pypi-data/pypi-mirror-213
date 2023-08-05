# coding=utf-8
import unittest
from halring.date_time.halring_datetime import DatetimeUtil
from halring.common.halring_const_variable import ConstVariable


class TestDatetimeUtil(unittest.TestCase):

    def test_get_format_curr_datetime_001_valid_date(self):
        util = DatetimeUtil()
        time_stamp = util.get_format_curr_datetime(ConstVariable.FORMAT_DATETIME_MYSQL)
        print("time_stamp: ", time_stamp, type(time_stamp))
        assert len(time_stamp) == 21

    def test_calc_datetime_001_valid_date(self):
        util = DatetimeUtil()
        input_date = "20190101"
        time_stamp = util.calc_datetime(input_date)
        print("time_stamp: ", time_stamp, type(time_stamp))
        assert len(time_stamp) == 21
        assert input_date in time_stamp

    def test_calc_datetime_002_invalid_date(self):
        util = DatetimeUtil()
        input_date = "99999999"
        time_stamp = util.calc_datetime(input_date)
        print("time_stamp: ", time_stamp, type(time_stamp))
        assert len(time_stamp) == 21
        assert input_date in time_stamp

    def test_calc_datetime_003_invalid_date_alpha(self):
        util = DatetimeUtil()
        input_date = "ABCDEFGH"
        time_stamp = util.calc_datetime(input_date)
        print("time_stamp: ", time_stamp, type(time_stamp))
        assert len(time_stamp) == 21
        assert input_date in time_stamp

    def test_calc_datetime_004_length_less(self):
        util = DatetimeUtil()
        input_date = "2019010"
        time_stamp = util.calc_datetime(input_date)
        print("time_stamp: ", time_stamp, type(time_stamp))
        assert len(time_stamp) != 21
        assert input_date in time_stamp

    def test_calc_datetime_005_length_more(self):
        util = DatetimeUtil()
        input_date = "201901010"
        time_stamp = util.calc_datetime(input_date)
        print("time_stamp: ", time_stamp, type(time_stamp))
        assert len(time_stamp) != 21
        assert input_date in time_stamp

    def test_conv_datetime_to_timestamp_006_ok(self):
        util = DatetimeUtil()
        orgi_datetime = "2020-10-12 14:19:31"
        orgi_format_string = ConstVariable.FORMAT_DATETIME_MYSQL
        new_timestamp = util.conv_datetime_to_timestamp(orgi_datetime, orgi_format_string)
        print("new_timestamp: {0}".format(new_timestamp))
        assert new_timestamp.__eq__("1602483571")

    def test_conv_timestamp_to_datetime_007_ok(self):
        util = DatetimeUtil()
        orgi_datetime = "2020-10-12 14:19:31"
        orgi_format_string = ConstVariable.FORMAT_DATETIME_MYSQL
        new_timestamp = util.conv_datetime_to_timestamp(orgi_datetime, orgi_format_string)
        print("new_timestamp: {0}".format(new_timestamp))
        new_datetime = util.conv_timestamp_to_datetime(new_timestamp,
                                                       new_format_string=ConstVariable.FORMAT_DATETIME_MYSQL)
        print("new_datetime: {0}".format(new_datetime))
        assert new_timestamp.__eq__(orgi_datetime)

    def test_drift_datetime_mysql_008_ok_forward(self):
        util = DatetimeUtil()
        format_string = ConstVariable.FORMAT_DATETIME_MYSQL
        orgi_datetime = "2020-10-12 14:19:31"
        drift_direction = ConstVariable.DRIFT_DIRECTION_FORWARD
        drift_second = 5
        drift_datetime = util.drift_datetime_mysql(format_string, orgi_datetime, drift_direction, drift_second)
        print("orgi_datetime: {0} drift_datetime: {1}".format(orgi_datetime, drift_datetime))
        assert drift_datetime.__eq__("2020-10-12 14:19:26")

    def test_drift_datetime_mysql_008_ok_backward(self):
        util = DatetimeUtil()
        format_string = ConstVariable.FORMAT_DATETIME_MYSQL
        orgi_datetime = "2020-10-12 14:19:31"
        drift_direction = ConstVariable.DRIFT_DIRECTION_BACKWARD
        drift_second = 65
        drift_datetime = util.drift_datetime_mysql(format_string, orgi_datetime, drift_direction, drift_second)
        print("orgi_datetime: {0} drift_datetime: {1}".format(orgi_datetime, drift_datetime))
        assert drift_datetime.__eq__("2020-10-12 14:20:36")
