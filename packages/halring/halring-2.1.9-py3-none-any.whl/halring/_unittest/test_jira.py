# -*- coding:UTF-8 -*-
import unittest
from halring.jira_lib.halring_jira import JiraUtil

debug = False
if debug:
    jira_auth = ("root", "qq2921481", "http://82.157.57.43:18080/")
    jfrog_auth = ('pei.xiaodong', 'AP9KPnDRLTrWHEhuYVGBjgReVFm')
else:
    jira_auth = ("admin", "Sseadmin123", "http://10.112.6.11:8080/jira")
    jfrog_auth = ("admin", "AP4nvanCDKm8eZM6F1VLUzgv2kK")


class TestJira(unittest.TestCase):

    def setUp(self):
        self.jira_cli = JiraUtil(*jira_auth)
        self.jira_cli.login()

    def test_a_jira_connect(self):
        self.assertTrue(self.jira_cli.login())

    def test_b_create_jira(self):
        new_model = self.jira_cli.create_issue({
            'project': {'id': '10585'},  # 项目: 门禁开发测试  10585 or 门禁系统 10604
            'summary': f"需求概要",  # 概要
            'description': '需求描述信息',
            # 'issuetype': {'id': '10501'},  # issuetype 表 -> 10307 -> 准出问题单 10501-> 开发任务是10501
            'issuetype': {"name": "开发任务"},  # 问题类型
            'priority': {'id': '3'},  # 优先级: 中
            'assignee': {'name': 'pei.xiaodong'},  # 经办人必须存在,一般跟域帐号
            # 'reporter': {'name': 'admin'},
            'duedate': '2023-02-03',   #　到期日　必填字段
            'customfield_11002': [{"name": "1.10.1"}],  # 1.10.1 基线版本必须存在字段
            'customfield_10857': [{"name": "pei.xiaodong"}],  # 开发者
            'fixVersions':  [{"name": "1.1.1"}]   # 1.1.1 修复版本必须存在字段
         })
        globals()['new_model'] = new_model
        print("test_create_jira !!!!--->", new_model.key)
        self.assertIsNotNone(new_model)

    def test_c_jira_get_info(self):
        jira_model = self.jira_cli.issue(globals()['new_model'].key)
        self.assertIsNotNone(jira_model)

    def test_d_update_jira_info(self):
        key = globals()['new_model'].key
        result = self.jira_cli.update_issue(key, {"assignee": {'name': "peihl"}})
        self.assertTrue(result)

    def test_e_del_jira_info(self):
        key = globals()['new_model'].key
        globals()['new_model'].delete()
        not_exists = None
        try:
            self.jira_cli.issue(key)
        except:
            not_exists = True
        else:
            not_exists = False
        self.assertTrue(not_exists)


