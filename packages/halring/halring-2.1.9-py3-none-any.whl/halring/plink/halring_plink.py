# coding=utf-8
import os
from loguru import logger
from ftp.halring_ftp import FtpUtil
from common.halring_common import ConstVariable


class PlinkUtil(ConstVariable):
    """
    Plink with Putty
    Author: xqzhou
    """
    def __init__(self, ip, user, pwd, cmd):
        self._ip = ip
        self._user = user
        self._pwd = pwd
        self._cmd = cmd
        self._plink_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "putty" + os.sep

    def plink_mass_execute(self, tool_mode=''):
        rslt_list = []
        if '|' in self._ip and '|' in self._user and '|' in self._pwd:
            ip_list   = self._ip.split('|')
            user_list = self._user.split('|')
            pwd_list = self._pwd.split('|')
            if ip_list.__len__() == user_list.__len__() == pwd_list.__len__():
                logger.info("plink mass execute. {0}".format(tool_mode))
                for i in  range(0, ip_list.__len__()):
                    if tool_mode.__eq__(self.VMS_SPECIAL):
                        curr_rslt = self.plink_execute_vms(ip_list[i], user_list[i], pwd_list[i])
                    else:
                        curr_rslt = self.plink_execute(ip_list[i], user_list[i], pwd_list[i])
                    rslt_list.append(curr_rslt)
            else:
                logger.error("plink mass execute param count diffience ip={0} user={1} pwd={2}".format(self._ip, self._user, self._pwd))
                assert False
        else:
            logger.info("plink single execute. {0}".format(tool_mode))
            if tool_mode.__eq__(self.VMS_SPECIAL):
                curr_rslt = self.plink_execute_vms()
            else:
                curr_rslt = self.plink_execute()
            rslt_list.append(curr_rslt)
        rslt_list_cnt = rslt_list.__len__()
        if rslt_list_cnt < 0:
            logger.error("")
            assert False
        elif 0 < rslt_list_cnt <= 1:
            return rslt_list[0]
        else:
            first_item = ''
            for item in rslt_list:
                if first_item.__eq__(''):
                    first_item = item
                    break
                else:
                    if first_item.__ne__(item):
                        logger.error("plink mass execute mass result diffience. first result: {0} curr result {1}".format(first_item, item))
                        assert False
            logger.debug("plink mass execute multi result consistency")
        return first_item

    def plink_execute(self, input_ip='', input_user='', input_pwd=''):
        """
        1.plink remote execute command
        :return:
        """
        if input_ip.__eq__(''):
            input_ip = self._ip
        if input_user.__eq__(''):
            input_user = self._user
        if input_pwd.__eq__(''):
            input_pwd = self._pwd
        execute_cmd = "@echo y|" + str(self._plink_path) + "plink.exe -pw " + str(input_pwd) + " " + str(input_user) + "@" + str(input_ip) + " \"" + str(self._cmd) + "\""
        logger.debug("old_execute_cmd: {0}".format(execute_cmd))
        # replace ' to \\\'"
        new_execute_cmd = ""
        split_symbol = "'"
        if split_symbol in execute_cmd:
            execute_cmd_list = execute_cmd.split(split_symbol)
            for item in execute_cmd_list:
                new_execute_cmd = item if new_execute_cmd.__eq__("") else new_execute_cmd + "\\\"" + item
            logger.debug("new_execute_cmd: {0}".format(new_execute_cmd))
            execute_cmd = new_execute_cmd
        logger.info("execute_cmd: {0}".format(execute_cmd))
        with os.popen(execute_cmd, 'r') as execute_cmd_hndl:
            execute_rtn = execute_cmd_hndl.read()
            logger.info("execute_rtn: {0}".format(execute_rtn))
            execute_cmd_hndl.close()
        return execute_rtn

    def plink_execute_vms(self, input_ip='', input_user='', input_pwd=''):
        '''
        1.execute script and gen result on remote
        2.ftp get result from remote
        3.read result
        4.return result
        :return:
        '''
        if input_ip.__eq__(''):
            input_ip = self._ip
        if input_user.__eq__(''):
            input_user = self._user
        if input_pwd.__eq__(''):
            input_pwd = self._pwd
        if "172.23.1.54" in input_ip or "172.23.1.55" in input_ip:
            tool_plink_remote_on_vms = "@DTOOLS:plink_remote_on_vms.com"
        else:
            tool_plink_remote_on_vms = "@back01$:[air.script]plink_remote_on_vms.com"
        execute_cmd = "@echo y|" + str(self._plink_path) + "plink.exe -pw " + str(input_pwd) + " " + str(input_user) + "@" + str(input_ip) + " \" " + tool_plink_remote_on_vms + " \\\"" + self._cmd + "\\\"\""
        logger.info("execute_cmd: {0}".format(execute_cmd))
        with os.popen(execute_cmd, 'r') as execute_cmd_hndl:
            execute_rtn = execute_cmd_hndl.read()
            logger.info("execute_rtn: {0}".format(execute_rtn))
            execute_cmd_hndl.close()

        local_path  = self._plink_path
        result_name = "PLINK_REMOTE_RESULT.LOG"
        if "172.23.1.54" in input_ip or "172.23.1.55" in input_ip:
            remote_path = "UTOOLS"
        else:
            remote_path = "TOFF$WORK_DIR"
        remote_result_file = "{0}:{1}".format(remote_path, result_name)
        local_result_file  = local_path + result_name
        logger.info("Get {0} from {1}".format(local_result_file, remote_result_file))

#        ftp_download_cmd = "@echo y|" + str(self._plink_path) + "pscp.exe -pw " + str(input_pwd) + " " + str(input_user) + "@" + str(input_ip) + ":" + str(remote_result_file) + " " + local_path
#        logger.info("ftp_download_cmd: {0}".format(ftp_download_cmd))
#        with os.popen(ftp_download_cmd, 'r') as ftp_download_cmd_hndl:
#            ftp_download_cmd_rtn = ftp_download_cmd_hndl.read()
#            logger.info("ftp_download_cmd_rtn: {0}".format(ftp_download_cmd_rtn))
#            ftp_download_cmd_hndl.close()

        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        result = ftputil.ftputil_download(remote_result_file, local_result_file, "ASC")
        assert (result == True)
        ftputil.ftputil_close()

        logger.info("Read in {0}".format(local_result_file))
        with open(local_result_file, "r") as script_result_hndl:
            rec_list = script_result_hndl.read()
            script_result_hndl.close()

        return rec_list