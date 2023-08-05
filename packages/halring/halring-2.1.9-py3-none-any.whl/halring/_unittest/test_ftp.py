# -*- coding:UTF-8 -*-
import unittest

from halring.ftp.halring_ftp import FtpUtil


class TestFtpUtil(unittest.TestCase):
    def test_001_connect_IP_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\se001"
        input_pwd = "senew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        result = ftputil.ftputil_connect()
        assert (result is True)
        ftputil.ftputil_close()

    def test_002_connect_IP_wrong(self):
        input_ip = "198.2.943.1"
        input_user = "sg\se001"
        input_pwd = "senew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        result = ftputil.ftputil_connect()
        assert (result is False)

    def test_003_connect_user_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\se001"
        input_pwd = "senew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        result = ftputil.ftputil_connect()
        assert (result is True)
        ftputil.ftputil_close()

    def test_004_connect_user_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sgse001"
        input_pwd = "senew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        result = ftputil.ftputil_connect()
        assert (result is False)

    def test_005_connect_pwd_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\se001"
        input_pwd = "senew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        result = ftputil.ftputil_connect()
        assert (result is True)
        ftputil.ftputil_close()

    def test_006_connect_pwd_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\se001"
        input_pwd = "sepwd001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        result = ftputil.ftputil_connect()
        assert (result is False)

    def test_031_upload_file_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\agxsjg120070313001.txt"
        destination = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313001.txt"  # 文件有后缀，文件名相同
        result = ftputil.ftputil_upload(source, destination)
        assert (result is True)
        ftputil.ftputil_close()

    def test_032_upload_file_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\agxsjg120070313001.txt"
        destination = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313002.txt"  # 文件有后缀，文件名不相同
        result = ftputil.ftputil_upload(source, destination)
        assert (result is True)
        ftputil.ftputil_close()

    def test_033_upload_file_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\ATP_BT_010120070313"
        destination = "/vol/incoming/q/48/mp106/sc001/ATP_BT_010120070313"  # 文件无后缀，文件名相同
        result = ftputil.ftputil_upload(source, destination)
        assert (result is True)
        ftputil.ftputil_close()

    def test_034_upload_file_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\ATP_BT_010120070313"
        destination = "/vol/incoming/q/48/mp106/sc001/ATP_BT_010120070314"  # 文件无后缀，文件名不相同
        result = ftputil.ftputil_upload(source, destination)
        assert (result is True)
        ftputil.ftputil_close()

    def test_034_2_upload_file_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\ATP_BT_010120070313"
        destination = "/vol/incoming/q/48/mp106/sc001/sc001/ATP_BT_010120070314"  # /mp106/sc001/sc001/不存在，自动创建
        result = ftputil.ftputil_upload(source, destination)
        assert (result is True)
        ftputil.ftputil_close()

    def test_035_upload_file_file_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\agxsjg120070313001.txt"
        destination = "/vol/incoming/q/48/mp106/sc111/agxsjg120070313002.txt"  # 目的路径不存在，无权限创建
        result = ftputil.ftputil_upload(source, destination)
        assert (result is False)
        ftputil.ftputil_close()

    def test_036_upload_file_dirct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\agxsjg120070313001.txt"
        destination = "/vol/incoming/q/48/mp106/sc001/"  # 目的路径是文件夹
        result = ftputil.ftputil_upload(source, destination)
        assert (result is True)
        ftputil.ftputil_close()

    def test_037_upload_file_dirct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\ATP_BT_010120070313"  # 源路径无文件后缀
        destination = "/vol/incoming/q/48/mp106/sc001/"
        result = ftputil.ftputil_upload(source, destination)
        assert (result is True)
        ftputil.ftputil_close()

    def test_037_2_upload_file_dirct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\agxsjg120070313001.txt"
        destination = "/vol/incoming/q/48/mp106/sc001/a/"  # 目的路径不存在的文件夹,创建/a/目录
        result = ftputil.ftputil_upload(source, destination)
        assert (result is True)
        ftputil.ftputil_close()

    def test_037_3_upload_file_dirct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\agxsjg120070313001.txt"
        destination = "/vol/incoming/q/48/mp106/sc001/a"  # 目的路径存在，当最后一个字符非\时，目的路径做目录处理
        result = ftputil.ftputil_upload(source, destination)
        assert (result == True)
        ftputil.ftputil_close()

    def test_037_4_upload_file_dirct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\agxsjg120070313001.txt"
        destination = "/vol/incoming/q/48/mp106/sc001/b"  # 目的路径不存在，当最后一个字符非\时，目的路径做文件处理
        result = ftputil.ftputil_upload(source, destination)
        assert (result is True)
        ftputil.ftputil_close()

    def test_038_upload_file_dirct_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\agxsjg120070313001.txt"
        destination = "/vol/incoming/q/48/mp106/sc121/"  # 目的路径不存在,无权限创建mp106/sc121
        result = ftputil.ftputil_upload(source, destination)
        assert (result == False)
        ftputil.ftputil_close()

    def test_039_upload_direct_file_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\"  # 源头路径是文件夹
        destination = "/vol/incoming/q/48/mp106/sc121/agxsjg120070313001.txt"
        result = ftputil.ftputil_upload(source, destination)
        assert (result == False)
        ftputil.ftputil_close()

    def test_040_upload_direct_file_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp"  # 源头路径是文件夹
        destination = "/vol/incoming/q/48/mp106/sc121/agxsjg120070313001.txt"
        result = ftputil.ftputil_upload(source, destination)
        assert (result == False)
        ftputil.ftputil_close()

    def test_041_upload_direct_direct_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp"
        destination = "/vol/incoming/q/48/mp106/sc121/"  # 目的路径不存在
        result = ftputil.ftputil_upload(source, destination)
        assert (result == False)
        ftputil.ftputil_close()

    def test_061_fileisexist_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        source = "E:\\temp\\ATP_BT_010120070313"  # 本地文件无后缀
        result = ftputil.ftputil_file_exist(source)
        assert (result == True)

    def test_062_fileisexist_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        source = "E:\\temp\\agxsjg120070313001.txt"  # 本地文件有后缀
        result = ftputil.ftputil_file_exist(source)
        assert (result == True)

    def test_063_fileisexist_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313001.txt"  # 文件有后缀
        result = ftputil.ftputil_file_exist(source, "REMOTE")
        assert (result == True)
        ftputil.ftputil_close()

    def test_064_fileisexist_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/ATP_BT_010120070313"  # 文件无后缀
        result = ftputil.ftputil_file_exist(source, "REMOTE")
        assert (result == True)
        ftputil.ftputil_close()

    def test_065_fileisexist_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        source = "E:\\temp\\agxsjg111120070313002.txt"  # 文件不存在
        result = ftputil.ftputil_file_exist(source)
        assert (result == False)

    def test_066_fileisexist_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/agxsjg121170313001.txt"  # 文件不存在
        result = ftputil.ftputil_file_exist(source, "REMOTE")
        assert (result == False)
        ftputil.ftputil_close()

    def test_067_fileisexist_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc002"  # 目的路径不存在
        result = ftputil.ftputil_file_exist(source, "REMOTE")
        assert (result == False)
        ftputil.ftputil_close()

    def test_068_fileisexist_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp002/sc001/"  # 路径是文件夹，非文件，报错
        result = ftputil.ftputil_file_exist(source, "REMOTE")
        assert (result == False)
        ftputil.ftputil_close()

    def test_091_dircetisexist_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\"
        result = ftputil.ftputil_direct_exist(source)
        assert (result == True)
        ftputil.ftputil_close()

    def test_092_dircetisexist(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp"
        result = ftputil.ftputil_direct_exist(source)
        assert (result == True)
        ftputil.ftputil_close()

    def test_093_dircetisexist_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\agxsjg120070313001.txt"  # 文件
        result = ftputil.ftputil_direct_exist(source)
        assert (result == False)
        ftputil.ftputil_close()

    def test_094_dircetisexist_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\XXXX"  # 不存在的路径
        result = ftputil.ftputil_direct_exist(source)
        assert (result == False)
        ftputil.ftputil_close()

    def test_095_dircetisexist_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/"
        result = ftputil.ftputil_direct_exist(source, "REMOTE")
        assert (result == True)
        ftputil.ftputil_close()

    def test_096_dircetisexist_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001"
        result = ftputil.ftputil_direct_exist(source, "REMOTE")
        assert (result == True)
        ftputil.ftputil_close()

    def test_097_dircetisexist_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313001.txt"  # 文件非文件夹
        result = ftputil.ftputil_direct_exist(source, "REMOTE")
        assert (result == False)
        ftputil.ftputil_close()

    def test_098_dircetisexist_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc002/"  # 不存在
        result = ftputil.ftputil_direct_exist(source, "REMOTE")
        assert (result == False)
        ftputil.ftputil_close()

    def test_099_dircetisexist_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\se001"
        input_pwd = "senew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp002/se003/"  # 无权限访问
        result = ftputil.ftputil_direct_exist(source, "REMOTE")
        assert (result == False)
        ftputil.ftputil_close()

    def test_111_download_file_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313001.txt"  # 文件有后缀
        destination = "E:\\temp\\agxsjg120070313001.txt"
        result = ftputil.ftputil_download(source, destination)
        assert (result == True)
        ftputil.ftputil_close()

    def test_112_download_file_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313001.txt"
        destination = "E:\\temp\\se001111111111111111111qztpx20070313001.flg"  # 文件重命名
        result = ftputil.ftputil_download(source, destination)
        assert (result == True)
        ftputil.ftputil_close()

    def test_113_dowmload_file_file_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313001.txt"
        destination = "E:\\temp\\txxxx\\agxsjg120070313003.txt"  # 目的路径不存在，则创建E:\temp\txxxx\
        result = ftputil.ftputil_download(source, destination)
        assert (result == True)
        ftputil.ftputil_close()

    def test_114_download__file_dirct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313001.txt"
        destination = "E:\\temp\\"
        result = ftputil.ftputil_download(source, destination)
        assert (result == True)
        ftputil.ftputil_close()

    def test_115_download_file_dirct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313001.txt"
        destination = "E:\\temp"
        result = ftputil.ftputil_download(source, destination)
        assert (result == True)
        ftputil.ftputil_close()

    def test_116_download_file_dirct_true(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313001.txt"
        destination = "E:\\temp\\XXX"  # 目的路径不存在且最后一个字符非\会被判断成文件
        result = ftputil.ftputil_download(source, destination)
        assert (result == True)
        ftputil.ftputil_close()

    def test_116_2_download_file_dirct_true(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313001.txt"
        destination = "E:\\temp\\XX\\"  # 目的路径不存在且最后一个字符为\会被判断成目录
        result = ftputil.ftputil_download(source, destination)
        assert (result == True)
        ftputil.ftputil_close()

    def test_117_download_dircet_file_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"

        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/"  # 下载文件夹
        destination = "E:\\xxx\\agxsjg120070313001.txt"
        result = ftputil.ftputil_download(source, destination)
        assert (result == False)
        ftputil.ftputil_close()

    def test_118_download_direct_file_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001"  # 下载文件夹
        destination = "E:\\xxx\\agxsjg120070313001.txt"
        result = ftputil.ftputil_download(source, destination)
        assert (result == False)
        ftputil.ftputil_close()

    def test_119_download_direct_dirct_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001"  # 下载文件夹
        destination = "E:\\temp\\"
        result = ftputil.ftputil_download(source, destination)
        assert (result == False)
        ftputil.ftputil_close()

    def test_120_download_file_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/ATP_BT_010120070313"  # 文件无后缀
        destination = "E:\\temp\\ATP_BT_010120070312"
        result = ftputil.ftputil_download(source, destination)
        assert (result == True)
        ftputil.ftputil_close()

    def test_121_download_file_direct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "/vol/incoming/q/48/mp106/sc001/ATP_BT_010120070313"  # 文件无后缀
        destination = "E:\\temp\\"
        result = ftputil.ftputil_download(source, destination)
        assert (result == True)
        ftputil.ftputil_close()

    def test_151_check_dirct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc001/"  # 检查路径
        result = ftputil.ftputil_check(path)
        assert (result)
        ftputil.ftputil_close()

    def test_152_check_dirct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc001/"
        result = ftputil.ftputil_check(path)
        assert (result)
        ftputil.ftputil_close()

    def test_153_check_dirct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\se001"
        input_pwd = "senew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp002/"  # 包含子文件夹
        result = ftputil.ftputil_check(path)
        assert (result)
        ftputil.ftputil_close()

    def test_154_check_dirct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\se001"
        input_pwd = "senew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp002/se015"  # 文件夹为空
        result = ftputil.ftputil_check(path)
        assert (not result)
        ftputil.ftputil_close()

    def test_155_check_dirct_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc111"  # 文件夹不存在
        result = ftputil.ftputil_check(path)
        assert (not result)
        ftputil.ftputil_close()

    def test_156_check_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313002.txt"
        result = ftputil.ftputil_check(path)
        assert (result)
        ftputil.ftputil_close()

    def test_157_check_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc001/ATP_BT_010120070313"  # 文件无后缀
        result = ftputil.ftputil_check(path)
        assert (result)
        ftputil.ftputil_close()

    def test_158_check_file_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc111/se070sfrd20070313.txt"  # 文件不存在
        result = ftputil.ftputil_check(path)
        assert (not result)
        ftputil.ftputil_close()

    def test_159_check_file_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc001/ATP_BT_010120070314111111111"  # 文件不存在
        result = ftputil.ftputil_check(path)
        assert (not result)
        ftputil.ftputil_close()

    def test_181_delete_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc001/agxsjg120070313001.txt"  # 文件存在有后缀
        result = ftputil.ftputil_delete(path)
        assert (result)
        ftputil.ftputil_close()

    def test_182_delete_file_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc001/ATP_BT_010120070313"  # 文件存在无后缀
        result = ftputil.ftputil_delete(path)
        assert (result)
        ftputil.ftputil_close()

    def test_183_delete_file_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc001/se070sfrfd20070313.flg"  # 文件不存在
        result = ftputil.ftputil_delete(path)
        assert (not result)
        ftputil.ftputil_close()

    def test_184_delete_direct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc001/"  # 删除文件夹下所有文件
        result = ftputil.ftputil_delete(path)
        assert (result)
        ftputil.ftputil_close()

    def test_185_delete_direct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc001/"  # 文件夹是空
        result = ftputil.ftputil_delete(path)
        assert (result == True)
        ftputil.ftputil_close()

    def test_186_delete_direct_wrong(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        path = "/vol/incoming/q/48/mp106/sc111"  # 路径不存在
        result = ftputil.ftputil_delete(path)
        assert (result == False)
        ftputil.ftputil_close()

    # def test_187_delete_direct_right(self):
    #     input_ip = "198.2.3.1"
    #     input_user = "sg\se001"
    #     input_pwd = "senew001"
    #     ftputil = FtpUtil(input_ip, input_user, input_pwd)
    #     ftputil.ftputil_connect()
    #     path = "/vol/incoming/q/48/mp109/se001/"  #file  version is greater than 2
    #     result = ftputil.ftputil_delete(path)
    #     assert (result == True)
    #     ftputil.ftputil_close()

    def test_188_delete_direct_right(self):
        input_ip = "198.2.3.1"
        input_user = "sg\sc001"
        input_pwd = "scnew001"
        ftputil = FtpUtil(input_ip, input_user, input_pwd)
        ftputil.ftputil_connect()
        source = "E:\\temp\\ATP_BT_010120070313"
        path = "/vol/incoming/q/48/mp106/sc001/"  # 有子目录
        subpath = path + "a"
        ftputil._ftp.mkd(subpath)  # 创建path的有子目录
        ftputil.ftputil_upload(source, path)
        ftputil.ftputil_upload(source, subpath)
        result = ftputil.ftputil_delete(path)
        assert (result == True)
        ftputil.ftputil_close()
