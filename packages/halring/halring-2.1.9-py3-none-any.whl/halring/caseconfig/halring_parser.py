# -*- coding:utf-8 -*-
import configparser


class IniConfigParser(configparser.ConfigParser):
    """
    支持大小写的configparser
    from halring.caseconfig.parser import CaseConfigParser
    config = CaseConfigParser()
    config.read("a.ini")
    sections = config.sections()
    options = config.options(section_name)
    value = config.get(section_name, option_name)

    """

    def __init__(self):
        configparser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr
