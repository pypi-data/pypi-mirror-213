# -*- coding:utf-8 -*-
from halring.jira_lib.halring_jira import JiraUtil

a = 1
# r = pandas.("666666.txt")
# for x in r:
#     print(x)
# r = pandas.read_csv("666666.csv")
# for x in r:
#     print(x)
# p = 1
jira_auth = ("xqzhou", "Sse@dm1n", "http://10.112.6.11:8080/jira")
# jfrog_auth = ("admin", "AP4nvanCDKm8eZM6F1VLUzgv2kK")
j = JiraUtil(*jira_auth)
j.login()
with open("7777777.csv", encoding="utf-8") as f:
    r = f.readlines()

    for i, x in enumerate(r):
        if i == 0:
            continue
        x = x.replace("\n", "")
        row = x.split(",")
        ass_p1 = row[4]
        develop_p2 = row[5]
        task_name = row[0]
        begin_time = row[2]
        end_time = str(row[3])
        version = row[1]

        data = {
            'project': {'id': '12204'},  # 项目: 门禁开发测试  10585 or 门禁系统 10604 TPSC:12204
            'summary': task_name,  # 概要
            'description': f"{task_name}",
            # 'issuetype': {'id': '10501'},  # issuetype 表 -> 10307 -> 准出问题单 10501-> 开发任务是10501
            'issuetype': {"name": "开发任务"},  # 问题类型
            'priority': {'id': '3'},  # 优先级: 中
            'assignee': {'name': ass_p1},  # 经办人必须存在,一般跟域帐号
            # 'reporter': {'name': 'admin'},
            'duedate': end_time,  # 到期日　必填字段
            'customfield_11002': [{"name": version}],  # 1.10.1 基线版本必须存在字段
            'customfield_10857': [{"name": develop_p2}],  # 开发者
            'fixVersions': [{"name": version}]  # 1.1.1 修复版本必须存在字段
        }
        print(data)
        # new_issue_model = j.create_issue(data)
        # print(f"[{new_issue_model.key}]-[{new_issue_model.id}]")
        # pxd = 1

pxd = 1



# m = j.issue('LTNDTEST-1237')
# dic = {
#     'project': ''
# }
# j.create_issue()
# 门禁系统 10604
# 门禁开发测试  10585
# 以下选项必填：经办人，到期日，基线版本，修复的版本, 以下选项必填：经办人，到期日，基线版本，修复的版本

