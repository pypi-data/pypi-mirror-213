# -*- coding:UTF-8 -*-
import unittest
from halring.artifactory_lib.halring_artifactory_lib import ArtifactoryLibUtil


class TestPubArtifactoryLib(unittest.TestCase):
    def test_artifactorylibutil_001_search_001_recursive(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_search(
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/", "r", "a")
        print(result)
        # assert result == ['http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/3/1/',
        #                   'http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/3/2/']

    def test_artifactorylibutil_001_search_002_norecursive(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_search(
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/", "nr", "a")
        assert result == ['http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/1',
                          'http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/3',
                          'http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/中文目录']

    def test_artifactorylibutil_001_search_003_norecursive(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_search(
            "http://10.112.7.64:8082/artifactory/Release/NWF2020/", "nr", "d")
        assert result != []

    def test_artifactorylibutil_001_search_003_file(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_search(
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/DTD技术方案1.0.0版本.txt", "n", "a")
        assert result == ["http://10.112.7.64:8082/artifactory/Daily/testNGAir/DTD技术方案1.0.0版本.txt"]

    def test_artifactorylibutil_001_search_004_wrong(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_search(
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/smoke/中文目录3/", "r", "a")
        print(result)
        # assert result == "error"

    def test_artifactorylibutil_002_upload_001_upload_dir(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_upload("C:\\Users\\ygong.SSE\\Downloads\\lxl_test_2_backup.tar.gz",
                                                         "http://10.112.7.64:8082/artifactory/Release/NWF2020/BPC_10.10.10/10/编译/程序/")
        assert result == "success"

    def test_artifactorylibutil_002_upload_001_upload_file(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_upload("D:\\Tools\\test\\WS_FTP.LOG",
                                                         "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/中文目录")
        assert result == "success"

    def test_artifactorylibutil_002_upload_002_upload_wrong(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_upload("D:\\Tools\\test\\nothisdirectory",
                                                         "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/中文目录/")
        assert result == "error"

    def test_artifactorylibutil_002_download_001_download_dir(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_download("D:\\Tools\\test\\中文目录\\",
                                                           "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/中文目录")
        assert result == "success"

    def test_artifactorylibutil_002_download_002_download_file(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_download("D:\\Tools\\test\\",
                                                           "http://10.112.7.64:8082/artifactory/Daily/LANTERN/Lantern_2.3.0/%E5%8D%87%E7%BA%A7%E6%89%8B%E5%86%8C/%E5%87%86%E5%85%A5Lantern_2.3.0%E4%B8%8A%E7%BA%BF%E5%8D%87%E7%BA%A7%E6%89%8B%E5%86%8C.xlsx")
        assert result == "success"

    def test_artifactorylibutil_003_properties_001_setfile_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_set_property(
            "http://10.112.7.64:8082/artifactory/docker-dev/spcg/uums-schedule/2.6.2",
            "key2", "value")

        assert result == "success"

    def test_artifactorylibutil_003_properties_001_remove_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_remove_property(
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/中文目录/", "key")
        assert result == "error"

    def test_artifactorylibutil_003_properties_002_remove_error(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_remove_property(
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/中文目录/", "unexisted_key")
        assert result == "error"

    def test_artifactorylibutil_004_copy_001_dir_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_copy(
            "http://artifactory.test.com:8081/artifactory/Daily/LTNDTEST/&^$123fixversion7+A=/13/12/",
            "http://artifactory.test.com:8081/artifactory/Daily/LTNDTEST/&^$123fixversion7+A=/26/")
        assert result == "success"

    def test_artifactorylibutil_004_copy_002_file_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_copy(
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/DTD技术方案1.0.0版本.txt",
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/2/")
        assert result == "success"

    def test_artifactorylibutil_004_copy_003_filerename_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_copy(
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/DTD技术方案1.0.0版本.txt",
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/2/DTD技术方案2.txt")
        assert result == "success"

    def test_artifactorylibutil_004_move_001_file_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_move(

            "http://10.112.7.64:8082/artifactory/Daily/NADDONTEST/测试用2/",
            "http://10.112.7.64:8082/artifactory/Daily/NADDONTEST/测试用3"
        )
        assert result == "success"

    def test_artifactorylibutil_004_move_002_dir_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_move(
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/2",
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/中文目录1/")
        assert result == "success"

    def test_artifactorylibutil_004_move_002_filerename_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_move(
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/中文目录1/2/DTD技术方案1.0.0版本.txt",
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/中文目录1/2/3/DTD技术方案1.txt")
        assert result == "success"

    def test_artifactorylibutil_005_remove_001_file_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_remove(
            "http://10.112.7.64:8082/artifactory/Release/LTNDTEST/2.3.0.1-test/64/文档/"
        )
        assert result == "success"

    def test_artifactorylibutil_005_remove_002_dir_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_remove(
            "http://10.112.7.64:8082/artifactory/Daily/NADDONTEST/%E7%AC%AC%E4%B8%80%E5%B1%82%E7%9B%AE%E5%BD%95/%E7"
            "%AC%AC%E4%BA%8C%E5%B1%82%E7%9B%AE%E5%BD%95"
        )
        assert result == "success"

    def test_artifactorylibutil_005_remove_003_dir_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_remove(
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/ygong/中文目录1/"
        )
        assert result == "success"

    def test_artifactorylibutil_006_list_properties_success(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_list_properties(
            "http://10.112.7.64:8082/artifactory/Release/NWF2020/NWF2020/交付件检查单测专用版本/5/"
        )
        assert result != None

    def test_artifactorylibutil_007_copy_dst_dict_1(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_copy(
            "http://10.112.7.64:8082/artifactory/Daily/BPC/BPC_4.26.0/9/",
            "http://10.112.7.64:8082/artifactory/Release/BPC/BPC_4.26.0/5"
        )
        assert result == "success"

    def test_artifactorylibutil_007_copy_dst_dict_2(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_copy(
            "http://10.112.7.64:8082/artifactory/Daily/BPC/BPC_4.26.0/9/",
            "http://10.112.7.64:8082/artifactory/Release/BPC/BPC_4.26.0/5/"
        )
        assert result == "success"

    def test_artifactorylibutil_007_copy_dst_dict_3(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_copy(
            "http://10.112.7.64:8082/artifactory/Daily/BPC/BPC_10.10.10/20/",
            "http://10.112.7.64:8082/artifactory/Release/BPC/BPC_10.10.10/4"
        )
        assert result == "success"

    def test_artifactorylibutil_008_set_property_dist(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_set_property(
            "http://10.112.7.64:8082/artifactory/Release/BPC/BPC_10.10.10/4", "test_key", "test_value"
        )
        assert result == "success"

    def test_artifactorylibutil_009_upload_file_special_character_001(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)

        result = artifactory_lib_util.artifactory_upload(
            "D:\\GY\\特殊字符上传artifactory\\c#a.xlsx",
            "http://10.112.7.64:8082/artifactory/Delivery/NADDONTEST/交付件检查1/109/文档/c#a.xlsx"
        )
        assert result == "success"

    def test_artifactorylibutil_009_upload_file_special_character_002(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)

        result = artifactory_lib_util.artifactory_upload(
            "D:\\GY\\特殊字符上传artifactory\\c%a.xlsx",
            "http://10.112.7.64:8082/artifactory/Delivery/NADDONTEST/交付件检查1/109/文档/c#a.xlsx"
        )
        assert result == "error"

    def test_artifactorylibutil_009_upload_file_special_character_003(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)

        result = artifactory_lib_util.artifactory_upload(
            "D:\\GY\\特殊字符上传artifactory\\a~b`c!d@e$f^g&h(i)j-k—l[m]n{o}p+q=r.xlsx",
            "http://10.112.7.64:8082/artifactory/Delivery/NADDONTEST/交付件检查1/109/文档/c#a.xlsx"
        )
        assert result == "success"

    def test_create_dir(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        artifactory_lib_util.create_artifactory_dir("http://10.112.7.64:8082/artifactory/Daily/TTTTT/V1/中文 空格")

    def test_artifactorylibutil_010_general_path_exists_dist(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_path_exist(
            "http://10.112.7.64:8082/artifactory/DevRelease/LTNDTEST/test_v2.3.0_18/文档"
        )
        assert result == True

    def test_artifactorylibutil_011_file_md5_001(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_filepath_md5(
            "http://10.112.7.64:8082/artifactory/DevRelease/LTNATEST/test_v2.3.0_21/%E6%96%87%E6%A1%A3/%E5%BC%80%E5"
            "%8F%91%E5%AE%9E%E6%96%BD/%E5%BD%B1%E5%93%8D%E5%88%86%E6%9E%90%20%20%20%20%20%20%20~!%40%23%24%25%5E%26("
            ")_%2B%3D%7D%7B%5D%5B-%E5%89%AF%E6%9C%AC%20-%20%E5%89%AF%E6%9C%AC.xlsx"
        )
        print(result)

    def test_artifactorylibutil_011_file_md5_002(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_path_md5(
            "http://artifactory.test.com:8081/artifactory/DevRelease/LTNDTEST/test-2.3.0-18/程序/"
        )
        print(result)

    def test_artifactorylibutil_012_dir_state_001(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_path_stat(
            "http://10.112.7.64:8082/artifactory/Daily/NADDONTEST/%E7%AC%AC%E4%B8%80%E5%B1%82%E7%9B%AE%E5%BD%95/%E7"
            "%AC%AC%E4%BA%8C%E5%B1%82%E7%9B%AE%E5%BD%95"
        )
        print(str(result))

    def test_artifactorylibutil_014_copy_docker_001(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_promote_docker(
            "http://10.112.7.64:8082/artifactory/docker-test/spcg/uums_test_version1.0/1/uums-schedule/2.6.2",
            "http://10.112.7.64:8082/artifactory/docker-test/spcg/uums_test_version1.0/3/uums-schedule/2.6.2")
        print(result)

    def test_artifactorylibutil_015_docker_sha256(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_get_docker_sha256(
            "http://10.112.7.64:8082/artifactory/docker-test/naddontest/hhhhh/100/image-demo/0.1.0")
        print(result)

    def test_artifactorylibutil_016_deposit_move(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        if artifactory_lib_util.artifactory_path_exist(
                "http://10.112.7.64:8082/artifactory/Delivery/NADDONTEST/202008.v1/49/" + "程序/Archive/"):

            artifactory_lib_util.artifactory_move(
                "http://10.112.7.64:8082/artifactory/Delivery/NADDONTEST/202008.v1/49/" + "程序/Archive",
                "http://10.112.7.64:8082/artifactory/Delivery/NADDONTEST/202008.v1/49/" + "Archive/Deposit")

    def test_artifactorylibutil_017_docker_exist(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        # docker_exist = artifactory_lib_util.artifactory_path_exist(
        # "http://10.112.7.64:8082/artifactory/docker-dev/trdman/trdman-bond/ 20200818_107/")

        # docker_exist = artifactory_lib_util.artifactory_path_exist(
        # "http://10.112.7.64:8082/artifactory/Daily/TTTTT/V1/B A A C/V3/")
        docker_exist = artifactory_lib_util.artifactory_path_exist(
            "http://10.112.7.64:8082/artifactory/Daily/TTTTT/V1/A A A/VB/")
        print(str(docker_exist))

    def test_artifactorylibutil_018_new_path_set_property(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        my_path = "http://10.112.7.64:8082/artifactory/Daily/TTTTT/V1/A A A/VB/"
        artifactory_lib_util.create_artifactory_dir(my_path)
        # step_2 = artifactory_lib_util.artifactory_set_property(my_path,"testkey", "testvalue")
        # print(step_2)

    def test_artifactorylibutil_019_artifactory_latest_child_path(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        my_path = "http://10.112.7.64:8082/artifactory/Delivery/ITP/I040200/"
        print(artifactory_lib_util.artifactory_latest_child_path(my_path))

    def test_artifactorylibutil_020_artifactory_server2_exist(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        my_path = "http://10.112.7.10:80/artifactory/Daily/"
        print(artifactory_lib_util.artifactory_latest_child_path(my_path))

    # ========================= 冒烟用例 =========================

    def test_artifctorylibutil_100_artifactory_path_not_exist(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)

        my_path = "http://10.112.7.10:80/artifactory/Daily/testNGAir/smoke"
        if artifactory_lib_util.artifactory_path_exist(my_path):
            del_result = artifactory_lib_util.artifactory_remove(my_path)
            assert del_result == "success"
        else:
            exist_result = artifactory_lib_util.artifactory_path_exist(my_path)
            assert exist_result == False

    def test_artifctorylibutil_101_artifactory_del_path(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        my_path = "http://10.112.7.10:80/artifactory/Daily/testNGAir/smoke"
        artifactory_lib_util.create_artifactory_dir(my_path)
        exist_result = artifactory_lib_util.artifactory_path_exist(my_path)
        assert exist_result == True

    # 使用任一个本地文件
    def test_artifacotrylibutil_102_artifactory_upload(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        my_path = "http://10.112.7.10:80/artifactory/Daily/testNGAir/smoke/中文目录/"
        result = artifactory_lib_util.artifactory_upload("D:\\Tools\\test\\WS_FTP.LOG", my_path)
        # exist_result = artifactory_lib_util.artifactory_path_exist(my_path)
        assert result == "success"

    # 使用任一个本地目录
    def test_artifactorylibutil_102_artifactory_upload_dir(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        my_path = "http://10.112.7.10:80/artifactory/Daily/testNGAir/smoke/中文目录/"
        result = artifactory_lib_util.artifactory_upload("D:\\Tools\\test\\测试用目录\\", my_path)
        exist_result = artifactory_lib_util.artifactory_path_exist(my_path)
        assert result == "success"

    def test_artifacotrylibutil_103_artifactory_download(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        my_path = "http://10.112.7.10:80/artifactory/Daily/testNGAir/smoke/中文目录"
        result = artifactory_lib_util.artifactory_download("D:\\Tools\\test\\中文目录\\",
                                                           "http://10.112.7.10:80/artifactory/Daily/testNGAir/smoke/中文目录")
        assert result == "success"

    def test_artifactorylibutil_104_artifactory_copy_dir(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_copy(
            "http://10.112.7.64:8082/artifactory/Daily/TTTTT/中文 空格 百分号%/",
            "http://10.112.7.64:8082/artifactory/Daily/TTTTT/中文 空格 百分号%3")
        assert result == "success"

    def test_artifactorylibutil_105_artifactory_copy(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        my_path = "http://10.112.7.10:80/artifactory/Daily/testNGAir/smoke/2/DTD技术方案2.txt"
        result = artifactory_lib_util.artifactory_copy(
            "http://10.112.7.10:80/artifactory/Daily/testNGAir/DTD技术方案1.0.0版本.txt",
            my_path)
        exist_result = artifactory_lib_util.artifactory_path_exist(my_path)
        assert result == "success"

    def test_artifactorylibutil_106_artifactory_move(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        my_path = "http://10.112.7.10:80/artifactory/Daily/testNGAir/smoke/3/DTD技术方案3.txt"
        result = artifactory_lib_util.artifactory_move(
            "http://10.112.7.10:80/artifactory/Daily/testNGAir/smoke/2/DTD技术方案2.txt",
            my_path)
        exist_result = artifactory_lib_util.artifactory_path_exist(my_path)
        assert result == "success"

    def test_artifactorylibutil_107_artifactory_move_dir(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        result = artifactory_lib_util.artifactory_move(
            "http://10.112.7.64:8082/artifactory/DevRelease/LTNATEST/test_v2.3.0_21/文档/开发实施/",
            "http://10.112.7.64:8082/artifactory/Daily/testNGAir/smoke/中文目录3/a")
        assert result == "success"

    def test_artifactorylibutil_108_artifactory_aqc_gt2g(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        artifactory_path = "http://10.112.7.64:8082/artifactory/"
        item_find_condition = {
            "repo": "Release", "size": {"$gt": "2097152000"}, 'path': {"$match": "LTNDTEST/2.3.0-test/2/*"}
        }
        result = artifactory_lib_util.artifactory_query(artifactory_path, item_find_condition)
        print(str(result))

    def test_artifactorylibutil_109_artifactory_search_dir(self):
        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        artifactory_path = "http://10.112.7.64:8082/artifactory/DevRelease/LTNDTEST/test_v2.3.0_18/文档/"
        result = artifactory_lib_util.artifactory_search_dir(artifactory_path, 'r')
        print(str(result))

    def test_artifactorylibutil_110_artifactory_is_dir(self):

        user = "aqc001"
        password = "L@rtern@9c"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)

        # artifactory_path = 'http://10.112.7.64:8082/artifactory/DevRelease/LTNATEST/test_v2.3.0_21/%E6%96%87%E6%A1
        # %A3/%E5%BC%80%E5%8F%91%E5%AE%9E%E6%96%BD/%E5%BD%B1%E5%93%8D%E5%88%86%E6%9E%90%20%20%20%20%20%20%20~!%40%23
        # %24%25%5E%26()_%2B%3D%7D%7B%5D%5B-%E5%89%AF%E6%9C%AC%20-%20%E5%89%AF%E6%9C%AC.xlsx'
        # artifactory_path = 'http://10.112.7.64:8082/DevRelease/LTNATEST/test_v2.3.0_21/文档/开发实施/影响分析%20%20%20%20%20
        # %20%20~!@%23$%25%5E&()_+=%7D%7B%5D%5B-副本%20-%20副本.xlsx'
        artifactory_path = "http://10.112.7.64:8082/artifactory/DevRelease/LTNATEST/test_v2.3.0_21/文档/开发实施/o.txt"

        result = artifactory_lib_util.artifactory_path_isdir(artifactory_path)
        print(str(result))
