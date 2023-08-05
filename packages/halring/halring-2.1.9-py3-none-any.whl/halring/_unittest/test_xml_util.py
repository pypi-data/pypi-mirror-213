# -*- coding:UTF-8 -*-
import os
import unittest
from halring.xml_lib.halring_xml import XmlUtil


class TestXmlUtil(unittest.TestCase):
    def test_analysis_key_get_value(self):
        assert XmlUtil('./test.xml').analysis_key_get_value('city', 'neighbor') == 'city IS NOT EXIST'
        assert XmlUtil('./test.xml').analysis_key_get_value('country', 'neighbors') == 'neighbors IS ' \
                                                                                                     'NOT EXIST'
        assert XmlUtil('./test.xml').analysis_key_get_value(
            'country', 'neighbor') == 'Austria, MeilanLake, ERROR, NONE'

    def test_analysis_key_get_dict(self):
        assert XmlUtil('./test.xml').analysis_key_get_dict('city') == 'city IS NOT EXIST'
        assert XmlUtil('./test.xml').analysis_key_get_dict('zip') == {}
        assert XmlUtil('./test.xml').analysis_key_get_dict('countries') == {'name': 'Liechtenstein',
                                                                                          'year': '2008',
                                                                                          'gdppc': '141100',
                                                                                          'neighbor': ['Austria',
                                                                                                       'MeilanLake',
                                                                                                       'Singapore',
                                                                                                       'Maynila'],
                                                                                          'jiraserver': 'http://eqops.tc.com/jira',
                                                                                          'zip': 'NONE'}

    def test_analysis_dict(self):
        result = XmlUtil('./test.xml').analysis_key_get_dict('jira')
        print(str(result))

    def test_analysis_key_get_values(self):
        xml_util = XmlUtil(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/_uittest/test.xml")

        value_c = xml_util.analysis_key_get_values("country")
        print("value_c:" + str(value_c))
