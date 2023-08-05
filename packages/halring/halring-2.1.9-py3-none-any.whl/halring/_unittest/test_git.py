# -*- coding:UTF-8 -*-
import unittest

from halring.git.halring_git import GitUtil as GitUtil2


class TestGitUtil2(unittest.TestCase):

    def test_git_util_2_002(self):
        tool = GitUtil2("p27MP4VsyZP_F1NyfqcY")
        result = tool.git_get_commit_id("D:\\GitRepos\\bpc_FileTransport_Gateway\\")
        print(result)

    def test_git_util_2_003(self):
        tool = GitUtil2("p27MP4VsyZP_F1NyfqcY")
        # tool.git_clone("http://196.123.135.6:8001/tpbm_group/tpbm/", "D:\\test1\\pj\\bizdata")
        result = tool.git_diff("D:\\GitRepos\\test\\ngsp-web","22c9b5dfd78c52dfa0ba6ac9a7b9cb458650cac3", "a92c40b534cad75307192be762504dab58f21d8b")
        print(result)

        # tool.git_clear("D:\\test1\\pj\\bizdata")

    def test_git_util_2_004(self):
        tool = GitUtil2("p27MP4VsyZP_F1NyfqcY")
        result = tool.git_get_commit_id_byapi("http://196.123.135.6:8001/party-building/party-building.git","develop")
        print(result)

    def test_git_util_3_001(self):
        tool = GitUtil2("p27MP4VsyZP_F1NyfqcY")
        result = tool.git_clone_branch("http://196.123.135.6:8001/party-building/party-building.git","V3.7版本")
        print(result)   
