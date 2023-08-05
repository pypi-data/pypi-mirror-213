# -*- coding:UTF-8 -*-
import json


class JsonUtil(object):
    def __init__(self):
        pass

    @classmethod
    def jsonStrToDict(self, jsonStr):
        """
        json字符串转为python字典dict
        :param jsonStr: str
        :return: dict
        """
        return json.loads(jsonStr)

    @classmethod
    def dictToJsonObject(self, dict):
        """
        python字典dict转为json对象
        :param dict: dict
        :return: json object
        """
        return json.dumps(dict)

    @classmethod
    def dictToFile(self, dicts, filePath):
        """
        python字典dict转为文件存储
        :param dict: dict
        :param filePath: 存储的全路径 例如:D:\\2020\\map.dict
        :return: filePath
        """
        with open(filePath, 'w') as f:
            f.write(str(dicts))
            f.flush()
        return filePath

    @classmethod
    def jsonStrToFile(self, jsonStr, filePath):
        """
        json字符串转文件
        :param dict: dict
        :return: json object
        """
        with open(filePath, 'w') as f:
            json.dump(jsonStr, f)
        return filePath

    @classmethod
    def fileToJson(self, filePath):
        """
        json文件转为json对象
        :param dict: dict
        :return: json object
        """
        jsons=json.load(open(filePath))

        return str(jsons).replace("\'", "\"")

    @classmethod
    def loadJsonField(self, jsons, field):
        """
        从json对象或者json字符串中按字段提取值
        :param jsons: json格式数据
        :return: str
        """
        return json.loads(jsons)[field]


if __name__ == '__main__':
    jsonStr = "{\"title\": \"准入测试报告\", \"一、准入测试报告\": {\"系统\": \"NADDONTEST\", \"版本\": \"交付件检查2\", \"时间\": \"2020-05-07 17:20:33\", \"补丁\": [], \"结果\": \"不通过\"}, \"二、准入测试版本发现问题清单\": [{\"编号\": \"1\", \"分类\": \"版本交付单_该版本下无任何开发任务或问题单\", \"描述\": \" 无效交付\"}, {\"编号\": \"2\", \"分类\": \"版本交付单_交付类文档缺失文件名包含关联表的文档\", \"描述\": \"  缺失必须交付的关联表文档\"}, {\"编号\": \"3\", \"分类\": \"版本交付单_交付类文档缺失文件名包含影响分析的文档\", \"描述\": \"  缺失必须交付的影响分析文档\"}, {\"编号\": \"4\", \"分类\": \"版本交付单_交付类文档缺失文件名包含升级or用户的文档\", \"描述\": \"  缺失必须交付的升级or用户文档\"}], \"三、准入测试交付路径\": {\"交付单\": \"NADDONTEST-594 不触发交付件检查单2\", \"交付路径\": \"http://artifactory.test.com:8081/artifactory/Delivery/NADDONTEST/交付件检查2/8/\"}}"
    map = JsonUtil().jsonStrToDict(jsonStr)
    print(map)
    # JsonUtil().jsonStrToFile(jsonStr, "D:\\2020\\map.json")
    # to_json = JsonUtil().fileToJson("D:\\2020\\map.json")
    # print(to_json)
    # data = {'title': '测试json'}
    # jsons = JsonUtil().dictToJsonObject(data)
    # print(JsonUtil().loadJsonField(jsonStr, "title"))
    # path = "D:\\2020\\jsonStr.json"
    # jsonst = JsonUtil().fileToJson(path)
    # print(jsonst)
