# coding=utf-8
import os
import xml.etree.ElementTree as ET


class EnvConfigParser:
    """
    环境变量配置文件解析模块。
    根据配置文件信息获取环境变量字典。
    """
    def __init__(self, config_file_path):
        self.config_xml = config_file_path
        self.env_vars = dict()
        self.__parse_config()

    def get_evn_vars(self):
        return self.env_vars

    def get_env_value_by_key(self, key):
        return self.env_vars[key]

    def __parse_config(self):
        msg = "[ERROR] Failed to find config xml [%s]." % self.config_xml
        assert os.path.exists(self.config_xml), msg

        tree = ET.parse(self.config_xml)
        root = tree.getroot()  # root: env

        for node in root:
            key = node.tag.strip()
            value = node.text.strip()
            self.env_vars[key] = value


if __name__ == "__main__":
    config_xml = "..\\xls_file\配置文件\env_config.xml"
    parser = EnvConfigParser(config_xml)
    files = parser.get_evn_vars()
    for k, v in files.items():
        print("%s = %s" % (k, v))
