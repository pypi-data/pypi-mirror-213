# coding=utf-8
import os
import sys
import re
from loguru import logger
from .halring_const_variable import ConstVariable


class StringUtil(ConstVariable):
    """
    StringUtil
    Author: xqzhou
    """

    def string_replace(self, orig_string, selected_string, replace_string):
        """
        string replce string 字符串替换
        :param orig_string: 原始字符串
        :param selected_string:选中字符串
        :param replace_string:替换字符串
        :return: 最后结果
        """
        logger.debug("[{0}] old string [{1}]".format(sys._getframe().f_code.co_name, orig_string))
        tmp_list = str(orig_string).split(selected_string)
        new_string = ""
        for item in tmp_list:
            if new_string.__eq__(""):
                new_string = item
            else:
                new_string = new_string + replace_string + item
        logger.debug("[{0}] new string [{1}]".format(sys._getframe().f_code.co_name, new_string))
        return new_string

    def string_diff(self, left_string, right_string):
        """
        string content diff consisitency
        :param left_string: 待对比左面字符串
        :param right_string: 待对比右面字符串
        :return: True - consisitency, False - inconsisitency
        """
        rtn = True
        if (type(left_string) is not str or type(right_string) is not str):
            logger.error("[{0}]left or right string is not str {1} {2}".format(sys._getframe().f_code.co_name, type(left_string), type(right_string)))
            rtn = False
        else:
            left_string_len  = len(left_string)
            right_string_len = len(right_string)
            logger.debug("[{0}]Left  len:{1} content:[{2}]".format(sys._getframe().f_code.co_name, left_string_len,  left_string))
            logger.debug("[{0}]Right len:{1} content:[{2}]".format(sys._getframe().f_code.co_name, right_string_len, right_string))
            if left_string_len != right_string_len:
                logger.error("[{0}]left or right len is not equal".format(sys._getframe().f_code.co_name))
                rtn = False
            if left_string.__ne__(right_string):
                logger.error("[{0}]left or right content is not equal".format(sys._getframe().f_code.co_name))
                rtn = False
        return rtn

    def string_diff_step(self, left_string, right_string):
        """
        step string content diff , ignore something
        1.ignore tradenum: 17=90000003
        2.ignore timestamp: 60=20070312-15:37:23.000|42=20070312-15:37:22.000
        3.ignore remark: 58=x\0x01 after more space
        4.ignore orderid: 37=order_id|693=order_id
        5.ignore steplen: 9=X
        6.diff string
        :param left_string: 对比字符串1
        :param right_string: 对比字符串2
        :return:
        """
        rtn = True
        if (type(left_string) is not str or type(right_string) is not str):
            logger.error("[{0}]left or right string is not str".format(sys._getframe().f_code.co_name))
            rtn = False
        else:
            logger.debug("[{0}]old left_content:  [{1}]".format(sys._getframe().f_code.co_name, left_string))
            logger.debug("[{0}]old right_content: [{1}]".format(sys._getframe().f_code.co_name, right_string))
            left_string  = self.step_ignore_info(str(left_string))
            right_string = self.step_ignore_info(str(right_string))
            logger.debug("[{0}]new left_content:  [{1}]".format(sys._getframe().f_code.co_name, left_string))
            logger.debug("[{0}]new right_content: [{1}]".format(sys._getframe().f_code.co_name, right_string))
            rtn = self.string_diff(str(left_string), str(right_string))
        return rtn

    def step_ignore_info(self, insert_step):
        """
        step ignore something
        1.step ignore timestamp: 60=20070312-15:37:23.000 or 42=20070312-15:37:22.000, repalce YYYYMMDD-HH:MM:SS.000
        2.step ignore tradenum:  17=90000003, repalce X
        3.step ignore orderid:   37=1 or 693=2, repalce X
        4.step ignore steplen:   9=step_len, repalce X
        5.step ignore tail:     \0x01 clean after more space
        :param insert_step:
        :return:
        """
        logger.debug("[{0}]old insert_step: [{1}]".format(sys._getframe().f_code.co_name, insert_step))
        insert_new_step = ""
        insert_step_list = insert_step.split('')
        del insert_step_list[insert_step_list.__len__() - 1]
        for item in insert_step_list:
            item_list = item.split('=')
            if item_list[0].__eq__('60') or item_list[0].__eq__('42'):
                item = item_list[0] + "=YYYYMMDD-HH:MM:SS.000"
            if item_list[0].__eq__('17') or item_list[0].__eq__('37') or item_list[0].__eq__('693') or item_list[
                0].__eq__('9'):
                item = item_list[0] + "=X"
            insert_new_step = item + "" if insert_new_step is "" else insert_new_step + item + ""
        logger.debug("[{0}]new insert_step: [{1}]".format(sys._getframe().f_code.co_name, insert_new_step))
        return insert_new_step

    def step_autolen(self, insert_step):
        """
        # [STEP_AUTOLEN] => auto calc step len if chm len *2
        # 计算中文字符长度
        :param insert_step:
        :return:
        """
        insert_new_step = ""
        if self.STEP_AUTOLEN in insert_step:
            insert_step_list = insert_step.split('',1)
            insert_body_len = len(insert_step_list[1])
            logger.debug("[{0}] calc step body [{1}] {2}".format(sys._getframe().f_code.co_name, insert_step_list[1], insert_body_len))
            insert_body_chm_plus_len = len(re.findall('([\u4e00-\u9fa5])', insert_step))
            final_insert_step_body_len = insert_body_len + insert_body_chm_plus_len
            logger.debug("[{0}] insert_body_len = {1} insert_body_chm_plus_len = {2} final_insert_step_body_len = {3}".format(sys._getframe().f_code.co_name, insert_body_len, insert_body_chm_plus_len, final_insert_step_body_len))
            insert_new_step = "9=" + str(final_insert_step_body_len) + "" + insert_step_list[1]
        else:
            insert_new_step = insert_step
        return insert_new_step

    def step_null(self, insert_step):
        """
        # [STEP_NULL] => ignore step key=value
        :param insert_step:
        :return:
        """
        insert_new_step = ""
        if self.STEP_NULL in insert_step:
            logger.debug("[{0}]old insert_step: [{1}]".format(sys._getframe().f_code.co_name, insert_step))
            insert_sql_list = insert_step.split('')
            for item in insert_sql_list:
                if self.STEP_NULL in item:
                    pass
                else:
                    insert_new_step = item  if insert_new_step.__eq__("") else insert_new_step + "" + item
            logger.debug("[{0}]new insert_step: [{1}]".format(sys._getframe().f_code.co_name, insert_new_step))
        else:
            insert_new_step = insert_step
        return insert_new_step

    def string_replace_space(self, insert_string):
        """
        # [SPACE] => one space
        :param insert_string:
        :return:
        """
        logger.debug("[{0}] old insert_string: [{1}]".format(sys._getframe().f_code.co_name, insert_string))
        insert_new_string = insert_string.replace(self.SPACE, " ")
        logger.debug("[{0}] new insert_string: [{1}]".format(sys._getframe().f_code.co_name, insert_new_string))
        return insert_new_string

    def string_replace_empty(self, insert_string):
        """
        # [EMPTY] => NULL
        :param insert_string:
        :return:
        """
        logger.debug("[{0}] old insert_string: [{1}]".format(sys._getframe().f_code.co_name, insert_string))
        insert_new_string = insert_string.replace(self.EMPTY, "")
        logger.debug("[{0}] new insert_string: [{1}]".format(sys._getframe().f_code.co_name, insert_new_string))
        return insert_new_string

    def string_ignore_hex_zero(self, insert_string):
        """
        string_ignore_hex_zero
        :param insert_string:
        :return:
        """
        logger.debug("[{0}] old string: [{1}]".format(sys._getframe().f_code.co_name, insert_string))
        new_string = insert_string.replace(b'\x00'.decode(), "")
        logger.debug("[{0}] new string: [{1}]".format(sys._getframe().f_code.co_name, new_string))
        return new_string

    def string_generate(self, content, content_cnt):
        """
        generate string ,new string is content X content_cnt
        :param content:
        :param content_cnt:
        :return:
        """
        generate_string = ""
        for item in range(1, content_cnt+1):
            generate_string = generate_string + content
        logger.debug("[{0}] generate {1} X {2} generate_string: [{1}]".format(sys._getframe().f_code.co_name, content, content_cnt, generate_string))
        return generate_string

    def string_from_list_with_delimiter(self, list, delimiter="|"):
        """
        generate string from list
        use selected delimiter
        :param content:
        :param content_cnt:
        :return:
        """
        new_string = delimiter.join(list)
#        logger.debug("{0} {1} {2}".format(list,delimiter, new_string))
        return new_string

    def string_conv_list_to_str(self, orgi_list, item_prefix, item_postfix, item_delimiter):
        """
        string_conv_list_to_str
        conv list to string, list item add prefix and postfix and delimiter, generate new string
        """
        if isinstance(orgi_list, list):
            pass
        else:
            assert 0

        new_str = ""
        for orgi_list_item in orgi_list:
            new_list_item = item_prefix + orgi_list_item + item_postfix
            if len(new_str) == 0:
                new_str = new_list_item
            else:
                new_str = new_str + item_delimiter + new_list_item
        return new_str

    def string_ignore_single_quota(self, input_string):
        output_string = ""
        if "'" in input_string:
            output_string = input_string.replace("'","")
        else:
            output_string = input_string
        return output_string