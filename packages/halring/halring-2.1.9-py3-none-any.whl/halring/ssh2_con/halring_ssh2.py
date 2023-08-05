# coding=utf-8
import re

import datetime
import paramiko
import socket
from loguru import logger


class Ssh2Util(object):
    """
    Ssh2
    Author: lzhou
    """

    def __init__(self, host, username, password, port=22):
        self._ssh = None
        self._channel = None
        self._host = host
        self._username = username
        self._password = password
        self._port = port

    def connect(self):
        """
        ssh2 连接
        :return:
        """
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self._ssh.connect(hostname=self._host, port=self._port, username=self._username, password=self._password,
                              allow_agent=False, look_for_keys=False, timeout=10)
            info = '成功连接远程主机 host: %s  user: %s' % (self._host, self._username)
            logger.info(info)
            print('*' * 69)
        except:
            logger.error('远程连接失败')
            raise

    def disconnect(self):
        """
        ssh2 断开连接
        :return:
        """
        if self._ssh:
            self._ssh.close()
        print('*' * 69)
        logger.info('关闭远程连接')

    def read(self, timeout=1):
        """
        交互式shell的读方法，可维持会话状态，读取管道中的响应数据，
        直到超时时间内没有收到任何数据，则将之前读到的数据返回
        interactive shell func, rev output from the server, function would finish
        when raise a socket.timeout exception and return output
        :param timeout: Timeout in seconds. If this timeout is exceeded,
                        then an exception is raised.
        :return: output from the server
        :raises: A socket.timeout exception is raised on timeout.
        """
        if self._ssh is None:
            logger.error('未连接上远程主机，请先执行connect方法')
            return
        if self._channel is None:
            self._channel = self._ssh.invoke_shell(width=240)
        self._channel.settimeout(timeout)
        ret = self._channel.recv(65525)
        try:
            while True:
                ret += self._channel.recv(65525)
        except socket.timeout:
            try:
                result = ret.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    result = ret.decode('GB18030')
                except UnicodeDecodeError:
                    result = ret.decode('utf-8', errors='ignore')
            return result

    def send(self, cmd, timeout=10):
        """
        交互式shell的写方法，可维持会话状态，将执行指令写入管道，发送给远程主机
        interactive shell func, send the 'cmd' to remote host
        :param cmd: the instruction send to remote host
        :param timeout: Timeout in seconds. If this timeout is exceeded,
                         then an exception is raised.
        :return:
        :raises: A socket.timeout exception is raised on timeout.
        """
        if self._ssh is None:
            logger.error('未连接上远程主机，请先执行connect方法')
            return
        if self._channel is None:
            self._channel = self._ssh.invoke_shell(width=240)
        print('-' * 69)
        logger.debug('发送指令：%s' % cmd)
        self._channel.settimeout(timeout)
        cmd = cmd.encode() + b'\r'
        try:
            self._channel.send(cmd)
        except socket.timeout:
            logger.error('发送指令超时，检查指令是否为空')

    def exec_command(self, cmd, timeout=5):
        """
        远程执行指令，非交互式，不维持会话状态
        :param cmd: 需要执行的指令
        :param timeout: 超过该时间将立刻返回响应结果
        :return: 指令执行结果，包括响应消息、错误信息和命令状态码
        """
        std_in, std_out, std_err = self._ssh.exec_command(cmd)
        ret_out = std_out.read(65525)
        ret_err = std_err.read(65525)
        start_time = datetime.datetime.now()
        while not std_out.channel.exit_status_ready():
            runtime = datetime.datetime.now() - start_time
            if runtime.seconds >= timeout:
                break
            else:
                ret_out += std_out.read(65525)
                ret_err += std_err.read(65525)
        try:
            result_out = ret_out.decode('utf-8')
            result_err = ret_err.decode('utf-8')
        except UnicodeDecodeError:
            try:
                result_out = ret_out.decode('GB18030')
                result_err = ret_err.decode('GB18030')
            except UnicodeDecodeError:
                result_out = ret_out.decode('utf-8', errors='ignore')
                result_err = ret_err.decode('utf-8', errors='ignore')
        if std_out.channel.exit_status_ready:
            ret_status = std_out.channel.recv_exit_status()
        else:
            ret_status = -1
        return result_out, result_err, ret_status

    @staticmethod
    def find_expect(data, expect=']\\$'):
        """
        根据返回的结果，查找期望包含的数据
        :param data: 返回的结果
        :param expect: 期望包含的数据
        :return:
        """
        if re.search(expect, data):
            logger.info('找到预期响应\'%s\'：\n%s' % (expect, data))
            return True
        else:
            logger.info('未找到预期响应\'%s\'：\n%s' % (expect, data))
            return False

    def read_line(self, cmd_complete=None, timeout=5):
        """
        交互式shell的读方法，可维持会话状态，读取管道中的响应数据，
        按自定义buffersize读取数据并回显，可设置判断指令执行完毕的条件, 是否找到制定关键字
        直到超时时间内没有收到任何数据且未找到指令执行完毕的条件，则超时并退出
        interactive shell func, rev output from the server, function would finish
        when raise a socket.timeout exception and return output
        :param cmd_complete: the condition to judge the command is completed
        :param timeout: Timeout in seconds. If this timeout is exceeded,
                        then an exception is raised.
        :return: output from the server
        :raises: A socket.timeout exception is raised on timeout.
        """
        cmd_result = ""
        if self._ssh is None:
            logger.error('未连接上远程主机，请先执行connect方法')
            return False
        if self._channel is None:
            self._channel = self._ssh.invoke_shell(width=240)
        self._channel.settimeout(timeout)
        if cmd_complete is not None:
            try:
                while True:
                    ret = self._channel.recv(1000)
                    # move /r/n, if you want to remain /r/n, you can remove the method strip()
                    if re.search(cmd_complete, ret.decode('utf-8', errors='ignore').replace('\r\n', '')):
                        logger.info(ret.decode('utf-8', errors='ignore'))
                        cmd_result += ret.decode('utf-8', errors='ignore')
                        logger.info("执行成功")
                        return True, cmd_result
                    logger.info(ret.decode('utf-8', errors='ignore'))
                    cmd_result += ret.decode('utf-8', errors='ignore')
            except socket.timeout:
                logger.error("执行超时，未能找到预期结果:" + cmd_complete)
                return False, cmd_result
        else:
            try:
                while True:
                    ret = self._channel.recv(1000)
                    # move /r/n, if you want to remain /r/n, you can remove the method strip()
                    logger.info(ret.decode('utf-8', errors='ignore'))
                    cmd_result += ret.decode('utf-8', errors='ignore')
            except socket.timeout:
                logger.info("指令执行完成")
                return True, cmd_result

    def connect_judge(self):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self._ssh.connect(hostname=self._host, port=self._port, username=self._username, password=self._password,
                              allow_agent=False, look_for_keys=False, timeout=10)
            info = '成功连接远程主机 host: %s  user: %s' % (self._host, self._username)
            logger.info(info)
            print('*' * 69)
            return True
        except:
            logger.info('远程连接失败')
            return False


if __name__ == '__main__':
    ssh_tool = Ssh2Util('172.23.1.101', 'aqc01', 'NGTSCFG', port=22)
    # ssh_tool.connect()
    # def_level_expect = r"@DEV->|@WATER->|@REL->|@PROD->|@NEW->"
    # if ssh_tool.read_line(def_level_expect, 5):
    #     ssh_tool.send(r"def_level DEV")
    #     ssh_tool.read_line("DEV", 5)
    # ssh_tool.send("dir")
    # result = ssh_tool.read_line()
    # if result[0]:
    #     print("ok")
    # t = result[1].splitlines()
    # print(t)
    # ssh_tool.disconnect()
    # ssh_tool = Ssh2Util('197.1.19.1', 'NGTS_40', 'SHANGHAI', port=22)
    # ssh_tool.connect()
    # result1 = ssh_tool.read(5)
    # if ssh_tool.find_expect(result1, 'SELECTION :'):
    #     ssh_tool.send('q')
    #     result1 = ssh_tool.read(1)
    # if ssh_tool.find_expect(result1, 'CHOICE:'):
    #     ssh_tool.send('e')
    #     result1 = ssh_tool.read(1)
    # if ssh_tool.find_expect(result1, '\)\$'):
    #     ssh_tool.send('nob')
    #     result1 = ssh_tool.read(1)
    # ssh_tool.send('cd EzEI/bin')
    # result = ssh_tool.read()
    # print(result)
    # ssh_tool.send('./menu')
    # result = ssh_tool.read()
    # print(result)
    # ssh_tool.send('C')
    # result = ssh_tool.read()
    # print(result)
    # ssh_tool.send('2')
    # result = ssh_tool.read(3)
    # print(result)

    # ret = ssh_tool.read(5)
    # ssh_tool.find_expect(ret, 'SELECTION :')

    # ssh_tool.find_expect(ret, 'CHOICE:')
    # ssh_tool.find_expect(ret, '\\)\\$')
    # ssh_tool = Ssh2Util('197.1.133.1', 'ngts_47', 'shanghai')
    # ssh_tool.connect()
    # ret_out1, ret_err1, ret_status1 = ssh_tool.exec_command('MCR TOL$EXE:SHOWRB -INS 600000')
    # print(ret_out1)
    # ssh_tool.find_expect(result, '成交')
    # print(ssh_tool.exec_command("ls -l"))
    # out, err = ssh_tool.exec_command("ll")
    # print(out)
    # print(err)
    # print(ssh_tool.exec_command('ll'))
