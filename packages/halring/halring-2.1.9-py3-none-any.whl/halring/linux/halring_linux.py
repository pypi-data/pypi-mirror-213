# coding=utf-8
import paramiko

from ssh2_con.halring_ssh2 import Ssh2Util
from db_aqcdb.halring_db_aqcdb import DbAqcdbUtil
from common.halring_const_variable import ConstVariable
from common.halring_common import CommonUtil


class LinuxUtil(object):
    """
    传入主机名称, ip, 用户名, 密码
    """

    def __init__(self, host_name, ip, user, password):
        self._host_name = host_name
        self._ip = ip
        self._user = user
        self._password = password
        self._ssh2_ins = Ssh2Util(self._ip, self._user, self._password)

        self._aqcdb_ip = ConstVariable.AQCDB_TESTENV_IP
        self._aqcdb_ins = ConstVariable.AQCDB_TESTENV_INSTANCE_AQCDB_TEST
        self._dau = DbAqcdbUtil(self._aqcdb_ip, self._aqcdb_ins)

        # 主机内存阀值字典：KEY=HOST|MEM|DESC VALUE=THRESHOLD_INFO
        self._host_mem_threshold_dict = self._dau.get_host_resource_info_used_threshold_from_aqcdb_by_type(
            ConstVariable.RESOURCE_TYPE_MEM)
        # 主机磁盘阀值字典：KEY=HOST|DISK|DIR VALUE=THRESHOLD_INFO
        self._host_disk_threshold_dict = self._dau.get_host_resource_info_used_threshold_from_aqcdb_by_type(
            ConstVariable.RESOURCE_TYPE_DISK)

    def connect_to_host(self):
        self._ssh2_ins.connect()

    def disconnect_to_host(self):
        self._ssh2_ins.disconnect()

    def linux_exec_command(self, cmd):
        return self._ssh2_ins.exec_command(cmd)

    def get_project_version_backup_package(self, project, version):
        """
        获取某个项目某个版本下的备份包地址
        :param project:
        :param version:
        :return:
        """
        pass

    def get_linux_cpu_free(self):
        """
        获取主机空闲的cpu
        :return:
        """
        cmd_line_cpu_free = "top -b -n 1 | grep %Cpu"
        result_host_cpu_free = self._ssh2_ins.exec_command(cmd_line_cpu_free)
        host_cpu_free = ' '.join(result_host_cpu_free[0].split()).split(",")[3].strip().split(" ")[0]
        print(host_cpu_free)

    def get_linux_mem_free(self):
        """
        获取主机空的内存
        :return:
        """
        pass

    def get_linux_disk_free(self, disk_name):
        """
        获取主机某个磁盘剩余的空间
        :return:
        """
        pass

    def clear_directory(self, directory):
        """
        清空某个目录的内容
        :param directory:
        :return:
        """
        pass

    def check_host_cpu_mem_disk_useable(self):
        """
        检查主机的可联通， cpu、 内存、磁盘空间可用性
        :return:<DICT> 主机cpu，内存，磁盘的状态
        """
        host_cpu_mem_disk_check = {}
        # 0 检查主机可连接
        result_connect = self._ssh2_ins.connect_judge()
        if result_connect:
            host_cpu_mem_disk_check[self._host_name + "|" + self._ip + " 主机连接状态"] = "可正常连接"
        else:
            host_cpu_mem_disk_check[self._host_name + "|" + self._ip + " 主机连接状态"] = "异常"
        # 1 抓取主机CPU剩余量 命令
        cmd_line_cpu_free = "top -b -n 1 | grep %Cpu"
        # 2 抓取主机内存剩余量 命令
        cmd_line_mem_free = "cat /proc/meminfo | grep MemFree | tr -cd \"[0-9]\""
        # 3 获取根目录下目录 命令
        cmd_line_disk_get_dir = "ls -l / | awk '/^d/ {print $NF}' | xargs"

        result_host_cpu_free = self._ssh2_ins.exec_command(cmd_line_cpu_free)
        host_cpu_free = ' '.join(result_host_cpu_free[0].split()).split(",")[3].strip().split(" ")[0]
        # print("host_cpu_free is " + str(result_host_cpu_free))
        if float(host_cpu_free) > 5.0:
            host_cpu_mem_disk_check["CPU"] = "OK"
            host_cpu_mem_disk_check["空闲CPU"] = str(host_cpu_free) + "%"
        else:
            host_cpu_mem_disk_check["CPU"] = "WARNING"
            host_cpu_mem_disk_check["空闲CPU"] = str(host_cpu_free) + "%"
            host_cpu_mem_disk_check["空闲CPU应大于"] = "5%"

        result_host_mem_free = self._ssh2_ins.exec_command(cmd_line_mem_free)
        host_mem_use = int(self._host_mem_threshold_dict[self._host_name+ "|MEM|SHM"].split("|")[0]) - round(int(result_host_mem_free[0]) / 1024 / 1024)
        host_mem_warn_threshold = int(self._host_mem_threshold_dict[self._host_name + "|MEM|SHM"].split("|")[0]) * int(self._host_mem_threshold_dict[self._host_name + "|MEM|SHM"].split("|")[1]) / 100
        # print("host_mem_use is " + str(host_mem_use) + ";" + "host_mem_warning_threshold is" + str(host_mem_warn_threshold))
        if (host_mem_use <= host_mem_warn_threshold):
            host_cpu_mem_disk_check["MEM"] = "OK"
            host_cpu_mem_disk_check["内存使用"] = str(host_mem_use) + "G"
        else:
            host_cpu_mem_disk_check["MEM"] = "WARNING"
            host_cpu_mem_disk_check["内存使用"] = str(host_mem_use) + "G"
            host_cpu_mem_disk_check["内存使用告警阀值"] = str(host_mem_warn_threshold) + "G"

        result_host_disk = self._ssh2_ins.exec_command(cmd_line_disk_get_dir)
        result_host_disk_list = str(result_host_disk[0]).split(" ")
        for val_result_host_dir in result_host_disk_list:
            # 拼接出获取磁盘大小的linux命令
            if val_result_host_dir in ("root", "opt", "home", "sse"):
                cmd_line_disk_get_dir_free_space = "df -h | grep " + val_result_host_dir
                result_host_disk_free_space = self._ssh2_ins.exec_command(cmd_line_disk_get_dir_free_space)
                result_host_disk_free_space_num = ' '.join(result_host_disk_free_space[0].split()).split(" ")[3]
                if ("G" in result_host_disk_free_space_num):
                    result_host_disk_free_space_num_final = result_host_disk_free_space_num[:-1]
                elif ("M" in result_host_disk_free_space_num):
                    result_host_disk_free_space_num_final = str(float(result_host_disk_free_space_num[:-1]) / 1024)
                else:
                    result_host_disk_free_space_num_final = 0

                disk_use = float(self._host_disk_threshold_dict[self._host_name + "|DISK|" + val_result_host_dir].split("|")[0]) - float(result_host_disk_free_space_num_final)
                host_disk_warn_threshold = float(self._host_disk_threshold_dict[self._host_name + "|DISK|" + val_result_host_dir].split("|")[0]) * float(self._host_disk_threshold_dict[self._host_name + "|DISK|" + val_result_host_dir].split("|")[1]) / 100
                # print("disk_name is " + val_result_host_dir + "disk_use is" + str(disk_use) + "," + "disk_warn_threshold is" + str(host_disk_warn_threshold))
                if (disk_use <= host_disk_warn_threshold):
                    host_cpu_mem_disk_check["DISK|" + val_result_host_dir] = "OK"
                    host_cpu_mem_disk_check[val_result_host_dir + " 磁盘使用量"] = str(round(disk_use,2)) + "G"
                else:
                    host_cpu_mem_disk_check["DISK|" + val_result_host_dir] = "WARNING"
                    host_cpu_mem_disk_check[val_result_host_dir + " 磁盘使用量"] = str(round(disk_use,2)) + "G"
                    host_cpu_mem_disk_check[val_result_host_dir + " 磁盘使用告警阀值"] = str(host_disk_warn_threshold) + "G"

        return host_cpu_mem_disk_check

    def check_host_java_vesion(self):
        """
        检查linux主机java版本
        :return:
        """
        check_java_version_dict = {}
        cmd_line_java_version = "java -version"
        try:
            result_java_version = self._ssh2_ins.exec_command(cmd_line_java_version)
            check_java_version_dict["java version"] = result_java_version[1].replace("\n", " ").split(" ")[2].replace("\"", "")
        except Exception:
            check_java_version_dict["java version"] = "未安装java运行环境"
        return check_java_version_dict

    def check_host_python_version(self):
        """
        检查linux类主机python版本
        :return:
        """
        check_python_version_dict = {}
        try:
            cmd_line_python_version = "python --version"
            result_python_version = self._ssh2_ins.exec_command(cmd_line_python_version)
            check_python_version_dict["python版本"] = result_python_version[1]
        except Exception:
            check_python_version_dict["python版本"] = "未安装python运行环境"
        return check_python_version_dict

    def check_host_sftp_connect(self):
        """
        检查linux主机sftp可联通
        :return:
        """
        check_sftp_connect_dict = {}
        try:
            t = paramiko.Transport(self._ip, 22)
            t.connect(username=self._user, password=self._password)
            sftp = paramiko.SFTPClient.from_transport(t)
            check_sftp_connect_dict["SFTP连接状态"] = "正常"
        except Exception:
            check_sftp_connect_dict["SFTP连接状态"] = "异常"
        return check_sftp_connect_dict
    

if __name__ == '__main__':
    lu = LinuxUtil("jenkins-server-2", "10.112.6.207", "root", "Fwq@glymm1")
    check_sftp_connect = lu.check_host_sftp_connect()
    CommonUtil().show_dict(check_sftp_connect, "check_sftp_connect")
