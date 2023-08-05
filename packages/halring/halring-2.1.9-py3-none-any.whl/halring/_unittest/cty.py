# -*- coding:UTF-8 -*-
from halring.jira_lib.halring_jira import JiraUtil

if __name__ == '__main__':
    jira_auth = ("admin", "Sseadmin123", "http://10.112.6.11:8080/jira")
    # jfrog_auth = ("admin", "AP4nvanCDKm8eZM6F1VLUzgv2kK")
    j = JiraUtil(*jira_auth)
    j.login()
    m = j.issue()
    pxd = 1


    # dic = {
    #     'project': ''
    # }
    # j.create_issue()
    # 门禁系统 10604
    # 门禁开发测试  10585
    # 以下选项必填：经办人，到期日，基线版本，修复的版本, 以下选项必填：经办人，到期日，基线版本，修复的版本
    # new_issue_model = j.create_issue({
    #     'project': {'id': '10585'},  # 项目: 门禁开发测试  10585 or 门禁系统 10604
    #     'summary': f"需求概要001",  # 概要
    #     'description': '需求描述信息001',
    #     # 'issuetype': {'id': '10501'},  # issuetype 表 -> 10307 -> 准出问题单 10501-> 开发任务是10501
    #     'issuetype': {"name": "开发任务"},  # 问题类型
    #     'priority': {'id': '3'},  # 优先级: 中
    #     'assignee': {'name': 'pei.xiaodong'},  # 经办人必须存在,一般跟域帐号
    #     # 'reporter': {'name': 'admin'},
    #     'duedate': '2023-02-03',   #　到期日　必填字段
    #     'customfield_11002': [{"name": "1.10.1"}],  # 1.10.1 基线版本必须存在字段
    #     'customfield_10857': [{"name": "peihl"}],  # 开发者
    #     'fixVersions':  [{"name": "1.1.1"}]   # 1.1.1 修复版本必须存在字段
    # })
    # debug = 1