# -*- coding:utf-8 -*-
import os
import re

from ftplib import FTP
from loguru import logger


class FtpUtil(object):
    """"
    ftp帮助类
    """

    FTPUTIL_WAY = "BIN"
    FTPUTIL_LOCALITY = "LOCAL"
    FTPUTIL_REMOTE = "REMOTE"

    def __init__(self, hostIp, userName, userPwd, ):
        self._hostIp = hostIp
        self._userName = userName
        self._userPwd = userPwd
        self._ftp = None

    def ftputil_connect(self):
        """
        ftp连接
        :return:
        """
        try:
            self._ftp = FTP(self._hostIp, self._userName, self._userPwd, timeout=3600)

        except Exception as e:
            logger.error("{}".format(e))
            return False
        else:
            return True

    # ftp退出
    def ftputil_close(self):
        self._ftp.quit()
        return True

    # 判断文件是否存在，不存在或是文件夹返回错误，文件存在返回正确
    def ftputil_file_exist(self, file, locality=FTPUTIL_LOCALITY):  # 判断文件是否存在
        # file:文件的绝对路径
        # locality：判断是检查本地还是远程服务器上的文件 ，取值"LOCAL" 或"REMOTE"
        if (locality.__eq__(FtpUtil.FTPUTIL_LOCALITY)):
            if (os.path.isfile(file)):
                # logger.info("{} is exist!".format(file))
                return True
            else:
                # logger.error("{} is not exist or is director!".format(file))
                return False
        else:
            if (self.ftputil_direct_exist(file, FtpUtil.FTPUTIL_REMOTE)):
                # logger.info("{} is director not file".format(file))
                return False
            else:
                result = self._ftp.nlst(file)
                if (re.match(r'.*no.such.file.or.directory.*', result[-1], re.I) or re.match(r'.*permission denied*',
                                                                                             result[-1], re.I)):
                    # logger.error(format(result[-1]))
                    return False
                else:
                    # logger.info(format(result[-1]))
                    return True

    # 判断文件夹是否存在
    def ftputil_direct_exist(self, path, locality=FTPUTIL_LOCALITY):
        # path:待检查的文件夹路径
        # locality：判断是检查本地还是远程服务器上的文件 ，取值"LOCAL" 或"REMOTE"
        if (locality.__eq__(FtpUtil.FTPUTIL_LOCALITY)):

            if (os.path.isdir(path)):
                # logger.info("The {} is exist!".format(path))
                return True
            else:
                # logger.error("The directory {} is not exist or permission denied !".format(path))
                return False
        else:
            try:
                self._ftp.cwd(path)
            except Exception as e:
                # logger.error("The directory {} is not exist or permission denied !".format(path))
                return False
            else:
                # logger.info("The {} is exist!".format(path))
                return True

    # 从本地上传文件到远程服务器
    def ftputil_upload(self, source, destination, transway=FTPUTIL_WAY):

        # source：源头路径（本地路径）
        # destination:目的路径（远程服务器路径）
        # transway:传输方式，BIN或ASCC传输，默认BIN传输

        if (self.ftputil_direct_exist(source, FtpUtil.FTPUTIL_LOCALITY)):  # 源路径是文件夹
            logger.error("[Error] You can't upload directory {}!".format(source))
            return False
        if not (self.ftputil_file_exist(source)):  # 源头路径的文件不存在
            logger.error("[Error]{} is not exist!".format(source))
            return False

        if (self.ftputil_direct_exist(destination, FtpUtil.FTPUTIL_REMOTE)):  # 目的路径是文件夹
            if (destination[0] != '/'):
                destination = "/" + destination

            if (destination[-1] != '/'):
                destination += "/"

            destination += source.split('\\')[-1]  # 目的路径是文件夹时，传输到目的路径的文件名与原文件名保持一致


        else:  # 无法区分是不存在的文件夹还是不存在的文件;因此目的路径是不存在文件夹会被处理成文件进行传输
            path = "/".join(destination.split('/')[:-1])

            if not (self.ftputil_direct_exist(path, FtpUtil.FTPUTIL_REMOTE)):
                # 上一层目录不存在则创建
                if (self.ftputil_create_dir(path, FtpUtil.FTPUTIL_REMOTE)):
                    # 以下情况针对不存在的以\结束的路径，在创建目录后，重新拼接路劲+文件名再传输
                    if (self.ftputil_direct_exist(destination, FtpUtil.FTPUTIL_REMOTE)):  # 目的路径是文件夹
                        if (destination[0] != '/'):
                            destination = "/" + destination

                        if (destination[-1] != '/'):
                            destination += "/"

                        destination += source.split('\\')[-1]  # 目的路径是文件夹时，传输到目的路径的文件名与原文件名保持一致
                else:
                    logger.error("There is not authority to create{}".format(path))
                    return False

        ftputil_upload_cmd = "stor " + destination

        if (transway.__eq__(FtpUtil.FTPUTIL_WAY)):  # BIN传输
            f = open(source, 'rb')
            try:
                self._ftp.storbinary(ftputil_upload_cmd, f)
                f.close()
            except Exception as e:
                f.close()
                logger.error(str(e))
                return False

        else:  # ASCII传输
            f = open(source, 'rb')
            try:
                self._ftp.storlines(ftputil_upload_cmd, f)
                f.close()
            except Exception as e:
                f.close()
                logger.error(str(e))
                return False

        logger.info("Upload {} to {} success!".format(source, destination))
        return True

    # 从远程服务器下载文件值本地
    def ftputil_download(self, source, destination, transway=FTPUTIL_WAY):

        # source：源头路径（远程服务器路径）
        # destination:目的路径（本地路径）
        # transway:传输方式，BIN或ASCC传输，默认BIN传输

        if (self.ftputil_direct_exist(source, FtpUtil.FTPUTIL_REMOTE)):  # 源头路径是文件夹
            logger.error("[Error] You can't download directory {}!".format(source))
            return False

        if not (self.ftputil_file_exist(source, FtpUtil.FTPUTIL_REMOTE)):  # 源头路径不存在
            logger.error("[Error]{} is not exist!".format(source))
            return False

        if (self.ftputil_direct_exist(destination, FtpUtil.FTPUTIL_LOCALITY)):  # 目的路径是文件夹
            if (destination[-1] != '\\'):
                destination += '\\'
            destination += source.split('/')[-1]


        else:  # 无法区分是不存在的文件夹还是不存在的文件;因此目的路径是不存在文件夹会被处理成文件进行传输
            path = "\\".join(destination.split("\\")[:-1])

            if not (self.ftputil_direct_exist(path)):
                # 上一层目录不存在则创建
                if (self.ftputil_create_dir(path, FtpUtil.FTPUTIL_LOCALITY)):
                    if (self.ftputil_direct_exist(destination, FtpUtil.FTPUTIL_LOCALITY)):  # 目的路径是文件夹
                        if (destination[-1] != '\\'):
                            destination += '\\'
                        destination += source.split('/')[-1]
                else:
                    logger.error("There is not authority to create{}".format(path))
                    return False

        ftputil_download_cmd = "retr " + source

        if (transway.__eq__(FtpUtil.FTPUTIL_WAY)):
            f = open(destination, 'wb')
            try:
                self._ftp.retrbinary(ftputil_download_cmd, f.write)
                f.close()
            except Exception as e:
                logger.error(str(e))
                f.close()
                return False

        else:
            f = open(destination, 'w')
            try:
                self._ftp.retrlines(ftputil_download_cmd, f.write)
                f.close()
            except Exception as e:
                logger.error(str(e))
                f.close()
                return False

        logger.info("Download {} to {} success!".format(source, destination))
        return True

    # 显示路径下文件、子目录以及子目录下的所有文件
    def ftputil_list_loop(self, path, files, locality=FTPUTIL_LOCALITY):
        # path: 路径
        # files:返回值，为“路径下文件、子目录以及子目录下的所有文件,包含自身路径”列表
        # locality：判断是检查本地还是远程服务器上的文件 ，取值"LOCAL" 或"REMOTE"
        if (locality.__eq__(FtpUtil.FTPUTIL_LOCALITY)):
            if ("\\" != path[-1]): path = path + "\\"
            items = os.listdir(path)
            directory = path
            files.append(directory)

            sub_items = items

            for item in sub_items:
                item = directory + item
                if self.ftputil_direct_exist(item):  # 是文件夹
                    self.ftputil_list_loop(item, files)
                elif self.ftputil_file_exist(item):  # 是文件
                    files.append(item)
                else:
                    item = item + '\\'
                    files.append(item)
        else:
            if ('/' != path[-1]): path = path + '/'
            items = self._ftp.nlst(path)
            # print("111111111111111111111")
            # print(items)
            # directory =  items[1][0:-1]   #与path相同
            # print(directory)

            if (items[0] != ''):
                directory = ''
                sub_items = items  # 所有子目录以及文件
            else:
                directory = path
                sub_items = items[2:]  # 所有子目录以及文件

                files.append(directory)

            for item in sub_items:
                item = directory + item
                if self.ftputil_direct_exist(item, FtpUtil.FTPUTIL_REMOTE):  # 可访问的子目录
                    self.ftputil_list_loop(item, files, FtpUtil.FTPUTIL_REMOTE)
                elif self.ftputil_file_exist(item, FtpUtil.FTPUTIL_REMOTE):  # 是文件
                    files.append(item)
                else:  # 无权限访问的子目录
                    item = item + '/'
                    files.append(item)

    # 显示路径下的所有文件，子目录，以及所有子目录下的文件,不包含本身路径
    def ftputil_list(self, path, locality=FTPUTIL_LOCALITY):
        # path:路径
        # locality：判断是检查本地还是远程服务器上的文件 ，取值"LOCAL" 或"REMOTE"
        files = []

        if (locality.__eq__(FtpUtil.FTPUTIL_LOCALITY)):

            self.ftputil_list_loop(path, files, FtpUtil.FTPUTIL_LOCALITY)
        else:
            self.ftputil_list_loop(path, files, FtpUtil.FTPUTIL_REMOTE)

        if (files[0] == ''):
            files = files[1:]
        return files

    # 检查远程服务器的文件是否存在或文件夹下的所有文件
    def ftputil_check(self, path):
        # path:远程服务器上路径，
        # path是文件,若文件存在返回文件名，文件不存在返回False;
        # path是文件夹，返回文件夹下所有文件，包含子目录及以下文件

        if (self.ftputil_direct_exist(path, FtpUtil.FTPUTIL_REMOTE)):  # path是文件夹
            files = self.ftputil_list(path, FtpUtil.FTPUTIL_REMOTE)
            if (not (files)):  # files is empty
                logger.error("[Error] {} is exist, but here is not file in {}".format(path, path))
            return files

        elif (self.ftputil_file_exist(path, FtpUtil.FTPUTIL_REMOTE)):  # path是文件
            if (self.ftputil_file_exist(path, FtpUtil.FTPUTIL_REMOTE)):
                logger.info("The {} is exist!".format(path))
                return path
            else:
                logger.error("The {} is not exist!".format(path))
                return False
        else:
            logger.error("The {} is not exist!".format(path))  # path不存在
            return False

    # 删除远程服务器路径下的文件或文件夹下的所有文件、子目录及以下文件
    def ftputil_delete(self, path):
        #:path:远程服务器路径，可取文件路径或者文件夹路径
        result = True
        if (self.ftputil_direct_exist(path, FtpUtil.FTPUTIL_REMOTE)):  # path是文件夹
            files = self.ftputil_list(path, FtpUtil.FTPUTIL_REMOTE)
            if not (files):  # 空
                logger.info("The {} is empty".format(path))
            else:
                directors = []
                for file in files:
                    if (self.ftputil_direct_exist(file, FtpUtil.FTPUTIL_REMOTE) and file.__ne__(path)):
                        directors.append(file)
                    else:
                        try:
                            self._ftp.delete(file)
                            logger.info("Delete {} is Succes!".format(file))
                        except Exception as e:
                            logger.error(str(e))
                            result = False

                if directors:
                    for director in directors:
                        try:
                            self._ftp.rmd(director)
                        except Exception as e:
                            logger.error(str(e))
                logger.info(" Delete all files in {}".format(path))

        elif (self.ftputil_file_exist(path, FtpUtil.FTPUTIL_REMOTE)):  # path是文件
            try:
                self._ftp.delete(path)
                logger.info("Delete {} is Succes!".format(path))
            except Exception as e:
                logger.error(str(e))
                result = False
        else:
            logger.error("The {} is not exist or has not authority to access!".format(path))
            result = False

        return result

    # 创建目录
    def ftputil_create_dir(self, path, locality=FTPUTIL_LOCALITY):
        # path:路径
        # locality：判断是本地还是远程服务器创建目录 ，取值"LOCAL" 或"REMOTE"

        if (locality.__eq__(FtpUtil.FTPUTIL_LOCALITY)):
            try:
                os.mkdir(path)
            except Exception as e:
                return False
        else:
            try:
                if ('/' == path[-1]): path = path[:-1]
                result = self._ftp.mkd(path)
            except Exception as e:
                return False
        return True
