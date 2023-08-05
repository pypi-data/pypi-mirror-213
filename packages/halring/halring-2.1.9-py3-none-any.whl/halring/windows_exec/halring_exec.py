# coding=utf-8
import os
import subprocess


class ExecUtil(object):
    """
    Exeute a program from python in Windows OS
    Author: xinwu
    """
    def __init__(self, cmd):
        self._cmd = cmd
        self._exe_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "exe" + os.sep

    def block_execute(self):
        """
        Exeute a program from python in Windows OS by blocking mode
        :return:
            console standard out
        """
        execute_cmd = self._exe_path + self._cmd
        print(execute_cmd)
        with os.popen(execute_cmd, "r") as execute_cmd_hndl:
            execute_rtn = execute_cmd_hndl.read()
            print(execute_rtn)
            execute_cmd_hndl.close()
        return execute_rtn

    def non_block_execute(self):
        """
        Exeute a program from python in Windows OS by non-blocking mode
        :return:
        """
        execute_cmd = self._exe_path + self._cmd
        p = subprocess.Popen(execute_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        '''while p.poll()==None:
            print(p.stdout.readline())
        print(p.returncode)'''


if __name__ == '__main__':
    exe = ExecUtil("startEzSTEP E:\FEAProduct\EzStepDTP\EzSTEP.exe")
    exe.block_execute()