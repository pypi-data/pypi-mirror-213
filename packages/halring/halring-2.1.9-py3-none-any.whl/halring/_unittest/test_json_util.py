# -*- coding:UTF-8 -*-
import unittest

from halring.json_lib.halring_json import JsonUtil
import os


class TestJsonUtil(unittest.TestCase):

    def test_json_util_001_jsonStrToDict(self):
        jsonStr = "{\"title\": \"准入测试报告\", \"一、准入测试报告\": {\"系统\": \"NADDONTEST\", \"版本\": \"交付件检查2\", \"时间\": \"2020-05-07 17:20:33\", \"补丁\": [], \"结果\": \"不通过\"}, \"二、准入测试版本发现问题清单\": [{\"编号\": \"1\", \"分类\": \"版本交付单_该版本下无任何开发任务或问题单\", \"描述\": \" 无效交付\"}, {\"编号\": \"2\", \"分类\": \"版本交付单_交付类文档缺失文件名包含关联表的文档\", \"描述\": \"  缺失必须交付的关联表文档\"}, {\"编号\": \"3\", \"分类\": \"版本交付单_交付类文档缺失文件名包含影响分析的文档\", \"描述\": \"  缺失必须交付的影响分析文档\"}, {\"编号\": \"4\", \"分类\": \"版本交付单_交付类文档缺失文件名包含升级or用户的文档\", \"描述\": \"  缺失必须交付的升级or用户文档\"}], \"三、准入测试交付路径\": {\"交付单\": \"NADDONTEST-594 不触发交付件检查单2\", \"交付路径\": \"http://artifactory.test.com:8081/artifactory/Delivery/NADDONTEST/交付件检查2/8/\"}}"
        JsonUtil.jsonStrToDict(jsonStr)

    def test_json_util_002_dictToJsonObject(self):
        data = {'title': '测试json'}
        JsonUtil.dictToJsonObject(data)

    def test_json_util_003_jsonStrToFile(self):
        jsonStr = "{\"title\": \"准入测试报告\", \"一、准入测试报告\": {\"系统\": \"NADDONTEST\", \"版本\": \"交付件检查2\", \"时间\": \"2020-05-07 17:20:33\", \"补丁\": [], \"结果\": \"不通过\"}, \"二、准入测试版本发现问题清单\": [{\"编号\": \"1\", \"分类\": \"版本交付单_该版本下无任何开发任务或问题单\", \"描述\": \" 无效交付\"}, {\"编号\": \"2\", \"分类\": \"版本交付单_交付类文档缺失文件名包含关联表的文档\", \"描述\": \"  缺失必须交付的关联表文档\"}, {\"编号\": \"3\", \"分类\": \"版本交付单_交付类文档缺失文件名包含影响分析的文档\", \"描述\": \"  缺失必须交付的影响分析文档\"}, {\"编号\": \"4\", \"分类\": \"版本交付单_交付类文档缺失文件名包含升级or用户的文档\", \"描述\": \"  缺失必须交付的升级or用户文档\"}], \"三、准入测试交付路径\": {\"交付单\": \"NADDONTEST-594 不触发交付件检查单2\", \"交付路径\": \"http://artifactory.test.com:8081/artifactory/Delivery/NADDONTEST/交付件检查2/8/\"}}"
        JsonUtil.jsonStrToFile(jsonStr, "C:\\myJson.json")
        # os.remove("C:\\myJson.json")

    def test_json_util_004_fileToJson(self):
        JsonUtil.fileToJson("C:\\myJson.json")
        os.remove("C:\\myJson.json")

    def test_json_util_005_loadJsonField(self):
        jsonStr = "{\"title\": \"准入测试报告\", \"一、准入测试报告\": {\"系统\": \"NADDONTEST\", \"版本\": \"交付件检查2\", \"时间\": \"2020-05-07 17:20:33\", \"补丁\": [], \"结果\": \"不通过\"}, \"二、准入测试版本发现问题清单\": [{\"编号\": \"1\", \"分类\": \"版本交付单_该版本下无任何开发任务或问题单\", \"描述\": \" 无效交付\"}, {\"编号\": \"2\", \"分类\": \"版本交付单_交付类文档缺失文件名包含关联表的文档\", \"描述\": \"  缺失必须交付的关联表文档\"}, {\"编号\": \"3\", \"分类\": \"版本交付单_交付类文档缺失文件名包含影响分析的文档\", \"描述\": \"  缺失必须交付的影响分析文档\"}, {\"编号\": \"4\", \"分类\": \"版本交付单_交付类文档缺失文件名包含升级or用户的文档\", \"描述\": \"  缺失必须交付的升级or用户文档\"}], \"三、准入测试交付路径\": {\"交付单\": \"NADDONTEST-594 不触发交付件检查单2\", \"交付路径\": \"http://artifactory.test.com:8081/artifactory/Delivery/NADDONTEST/交付件检查2/8/\"}}"
        JsonUtil.loadJsonField(jsonStr, "title")
