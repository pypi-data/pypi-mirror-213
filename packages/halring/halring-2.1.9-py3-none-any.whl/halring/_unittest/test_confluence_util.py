# -*- coding:UTF-8 -*-
import unittest
from halring.confluence.halring_confluence import ConfluenceUtil


class TestConfluenceUtil(unittest.TestCase):
    def test_get_page_body_value(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481')._get_page_version('核心后台公告栏', 'confluence rest api 测试')
        print(result)

    def test_jql_is_name(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481')._jql_is_name("陈颖")
        print(result)

    def test_get_space_key_001_exists(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481')._get_space_key_by_space_name(
            '核心后台公告栏')
        print(result)

    def test_get_space_key_002_not_exists(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481')._get_space_key_by_space_name(
            '核心后台公告')
        print(result)

    def test_create_table(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481')._create_table(['主机', '内存类型', '内存子类型', '主机内存配置大小(GB)'],
                                                              [['ASI391', 'MEM', 'SHM', '255'],
                                                               ['ASI392', 'MEM', 'SHM', '255'],
                                                               ['ASR791', 'MEM', 'SHM', '383'],
                                                               ['ASR792', 'MEM', 'SHM', '383'],
                                                               ['ASR793', 'MEM', 'SHM', '191'],
                                                               ['ASR794', 'MEM', 'SHM', '191'],
                                                               ['AST591', 'MEM', 'SHM', '383'],
                                                               ['AST592', 'MEM', 'SHM', '383'],
                                                               ['AST593', 'MEM', 'SHM', '383'],
                                                               ['AST594', 'MEM', 'SHM', '383'],
                                                               ['BST571', 'MEM', 'SHM', '128'],
                                                               ['BST572', 'MEM', 'SHM', '128'],
                                                               ['DSR761', 'MEM', 'SHM', '383'],
                                                               ['DSR762', 'MEM', 'SHM', '383'],
                                                               ['DSR763', 'MEM', 'SHM', '383'],
                                                               ['DSR764', 'MEM', 'SHM', '191'],
                                                               ['DST561', 'MEM', 'SHM', '383'],
                                                               ['DST562', 'MEM', 'SHM', '383'],
                                                               ['ESI301', 'MEM', 'SHM', '63'],
                                                               ['ESI302', 'MEM', 'SHM', '63'],
                                                               ['ESR701', 'MEM', 'SHM', '127'],
                                                               ['ESR702', 'MEM', 'SHM', '127'],
                                                               ['ESR703', 'MEM', 'SHM', '127'],
                                                               ['EST101', 'MEM', 'SHM', '71'],
                                                               ['EST102', 'MEM', 'SHM', '71'],
                                                               ['EST103', 'MEM', 'SHM', '127'],
                                                               ['HSI201', 'MEM', 'SHM', '15'],
                                                               ['HSI202', 'MEM', 'SHM', '127'],
                                                               ['HSI301', 'MEM', 'SHM', '191'],
                                                               ['HSI302', 'MEM', 'SHM', '191'],
                                                               ['HSR601', 'MEM', 'SHM', '15'],
                                                               ['HSR602', 'MEM', 'SHM', '47'],
                                                               ['HSR701', 'MEM', 'SHM', '383'],
                                                               ['HSR702', 'MEM', 'SHM', '383'],
                                                               ['HSR703', 'MEM', 'SHM', '383'],
                                                               ['HSR704', 'MEM', 'SHM', '383'],
                                                               ['HSR705', 'MEM', 'SHM', '383'],
                                                               ['HSR706', 'MEM', 'SHM', '255'],
                                                               ['HST001', 'MEM', 'SHM', '15'],
                                                               ['HST002', 'MEM', 'SHM', '31'],
                                                               ['HST101', 'MEM', 'SHM', '255'],
                                                               ['HST102', 'MEM', 'SHM', '255'],
                                                               ['HST103', 'MEM', 'SHM', '255'],
                                                               ['HST104', 'MEM', 'SHM', '255'],
                                                               ['HST105', 'MEM', 'SHM', '255'],
                                                               ['HST106', 'MEM', 'SHM', '127']])
        print(result)

    def test_append_confluence_list_001_success(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_list('核心后台公告栏', 'confluence rest api 测试',
                                                                       ['ASI391,MEM,SHM,255', 'ASI392,MEM,SHM,255',
                                                                        'ASR791,MEM,SHM,383', 'ASR792,MEM,SHM,383',
                                                                        'ASR793,MEM,SHM,191', 'ASR794,MEM,SHM,191',
                                                                        'AST591,MEM,SHM,383', 'AST592,MEM,SHM,383',
                                                                        'AST593,MEM,SHM,383', 'AST594,MEM,SHM,383',
                                                                        'BST571,MEM,SHM,128', 'BST572,MEM,SHM,128',
                                                                        'DSR761,MEM,SHM,383', 'DSR762,MEM,SHM,383',
                                                                        'DSR763,MEM,SHM,383', 'DSR764,MEM,SHM,191',
                                                                        'DST561,MEM,SHM,383', 'DST562,MEM,SHM,383',
                                                                        'ESI301,MEM,SHM,63', 'ESI302,MEM,SHM,63',
                                                                        'ESR701,MEM,SHM,127', 'ESR702,MEM,SHM,127',
                                                                        'ESR703,MEM,SHM,127', 'EST101,MEM,SHM,71',
                                                                        'EST102,MEM,SHM,71', 'EST103,MEM,SHM,127',
                                                                        'HSI201,MEM,SHM,15', 'HSI202,MEM,SHM,127',
                                                                        'HSI301,MEM,SHM,191', 'HSI302,MEM,SHM,191',
                                                                        'HSR601,MEM,SHM,15', 'HSR602,MEM,SHM,47',
                                                                        'HSR701,MEM,SHM,383', 'HSR702,MEM,SHM,383',
                                                                        'HSR703,MEM,SHM,383', 'HSR704,MEM,SHM,383',
                                                                        'HSR705,MEM,SHM,383', 'HSR706,MEM,SHM,255',
                                                                        'HST001,MEM,SHM,15', 'HST002,MEM,SHM,31',
                                                                        'HST101,MEM,SHM,255', 'HST102,MEM,SHM,255',
                                                                        'HST103,MEM,SHM,255', 'HST104,MEM,SHM,255',
                                                                        'HST105,MEM,SHM,255', 'HST106,MEM,SHM,127'])
        print(result)

    def test_append_confluence_dict_001_success(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_dict('核心后台公告栏', 'confluence rest api 测试', [
            {'主机': 'ASI391', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
            {'主机': 'ASI392', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
            {'主机': 'ASR791', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'ASR792', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'ASR793', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '191'},
            {'主机': 'ASR794', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '191'},
            {'主机': 'AST591', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'AST592', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'AST593', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'AST594', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'BST571', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '128'},
            {'主机': 'BST572', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '128'},
            {'主机': 'DSR761', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'DSR762', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'DSR763', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'DSR764', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '191'},
            {'主机': 'DST561', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'DST562', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'ESI301', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '63'},
            {'主机': 'ESI302', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '63'},
            {'主机': 'ESR701', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
            {'主机': 'ESR702', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
            {'主机': 'ESR703', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
            {'主机': 'EST101', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '71'},
            {'主机': 'EST102', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '71'},
            {'主机': 'EST103', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
            {'主机': 'HSI201', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '15'},
            {'主机': 'HSI202', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
            {'主机': 'HSI301', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '191'},
            {'主机': 'HSI302', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '191'},
            {'主机': 'HSR601', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '15'},
            {'主机': 'HSR602', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '47'},
            {'主机': 'HSR701', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'HSR702', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'HSR703', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'HSR704', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'HSR705', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
            {'主机': 'HSR706', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
            {'主机': 'HST001', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '15'},
            {'主机': 'HST002', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '31'},
            {'主机': 'HST101', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
            {'主机': 'HST102', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
            {'主机': 'HST103', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
            {'主机': 'HST104', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
            {'主机': 'HST105', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
            {'主机': 'HST106', '内存类型': 'MEM', '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
        ])
        print(result)

    def test_append_confluence_table_001_success(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_table('核心后台公告栏', 'confluence rest api 测试',
                                                                        ['主机', '内存类型', '内存子类型',
                                                                         '主机内存配置大小(GB)'], [
                                                                            ['ASI391', 'MEM', 'SHM', '255'],
                                                                            ['ASI392', 'MEM', 'SHM', '255'],
                                                                            ['ASR791', 'MEM', 'SHM', '383'],
                                                                            ['ASR792', 'MEM', 'SHM', '383'],
                                                                            ['ASR793', 'MEM', 'SHM', '191'],
                                                                            ['ASR794', 'MEM', 'SHM', '191'],
                                                                            ['AST591', 'MEM', 'SHM', '383'],
                                                                            ['AST592', 'MEM', 'SHM', '383'],
                                                                            ['AST593', 'MEM', 'SHM', '383'],
                                                                            ['AST594', 'MEM', 'SHM', '383'],
                                                                            ['BST571', 'MEM', 'SHM', '128'],
                                                                            ['BST572', 'MEM', 'SHM', '128'],
                                                                            ['DSR761', 'MEM', 'SHM', '383'],
                                                                            ['DSR762', 'MEM', 'SHM', '383'],
                                                                            ['DSR763', 'MEM', 'SHM', '383'],
                                                                            ['DSR764', 'MEM', 'SHM', '191'],
                                                                            ['DST561', 'MEM', 'SHM', '383'],
                                                                            ['DST562', 'MEM', 'SHM', '383'],
                                                                            ['ESI301', 'MEM', 'SHM', '63'],
                                                                            ['ESI302', 'MEM', 'SHM', '63'],
                                                                            ['ESR701', 'MEM', 'SHM', '127'],
                                                                            ['ESR702', 'MEM', 'SHM', '127'],
                                                                            ['ESR703', 'MEM', 'SHM', '127'],
                                                                            ['EST101', 'MEM', 'SHM', '71'],
                                                                            ['EST102', 'MEM', 'SHM', '71'],
                                                                            ['EST103', 'MEM', 'SHM', '127'],
                                                                            ['HSI201', 'MEM', 'SHM', '15'],
                                                                            ['HSI202', 'MEM', 'SHM', '127'],
                                                                            ['HSI301', 'MEM', 'SHM', '191'],
                                                                            ['HSI302', 'MEM', 'SHM', '191'],
                                                                            ['HSR601', 'MEM', 'SHM', '15'],
                                                                            ['HSR602', 'MEM', 'SHM', '47'],
                                                                            ['HSR701', 'MEM', 'SHM', '383'],
                                                                            ['HSR702', 'MEM', 'SHM', '383'],
                                                                            ['HSR703', 'MEM', 'SHM', '383'],
                                                                            ['HSR704', 'MEM', 'SHM', '383'],
                                                                            ['HSR705', 'MEM', 'SHM', '383'],
                                                                            ['HSR706', 'MEM', 'SHM', '255'],
                                                                            ['HST001', 'MEM', 'SHM', '15'],
                                                                            ['HST002', 'MEM', 'SHM', '31'],
                                                                            ['HST101', 'MEM', 'SHM', '255'],
                                                                            ['HST102', 'MEM', 'SHM', '255'],
                                                                            ['HST103', 'MEM', 'SHM', '255'],
                                                                            ['HST104', 'MEM', 'SHM', '255'],
                                                                            ['HST105', 'MEM', 'SHM', '255'],
                                                                            ['HST106', 'MEM', 'SHM', '127']])
        print(result)

    def test_append_confluence_image_001_success(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_image(
            '核心后台公告栏', 'confluence rest api 测试', "D:/Lighthouse.jpg")
        print(result)

    def test_append_jira_filter_001_success_body_is_url_no_columns(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_jira_filter(
            '核心后台公告栏', 'confluence rest api 测试', 'http://eqops.tc.com/jira/browse/JIRA-810')
        print(result)

    def test_append_jira_filter_002_fail_body_is_url_has_columns(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_jira_filter(
            '核心后台公告栏', 'confluence rest api 测试', 'http://eqops.tc.com/jira/browse/JIRA-810', 'key,summary,status')
        print(result)

    def test_append_jira_filter_003_success_body_is_jira_id_no_columns(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_jira_filter(
            '核心后台公告栏', 'confluence rest api 测试', 'JIRA-810')
        print(result)

    def test_append_jira_filter_004_fail_body_is_jira_id_has_columns(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_jira_filter(
            '核心后台公告栏', 'confluence rest api 测试', 'JIRA-810', 'key,summary,status')
        print(result)

    def test_append_jira_filter_005_success_body_is_jql_no_columns(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_jira_filter(
            '核心后台公告栏', 'confluence rest api 测试', 'project = JIRA服务台 AND resolution = 已完成')
        print(result)

    def test_append_jira_filter_004_success_body_is_jql_has_columns(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_jira_filter(
            '核心后台公告栏', 'confluence rest api 测试', 'project = JIRA服务台 AND resolution = 已完成', 'key,summary,status')
        print(result)

    def test_append_jira_filter_005_success_body_is_name_no_columns(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_jira_filter(
            '核心后台公告栏', 'confluence rest api 测试', '周修庆')
        print(result)

    def test_append_jira_filter_006_success_body_is_name_has_columns(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_jira_filter(
            '核心后台公告栏', 'confluence rest api 测试', '周修庆', 'key,summary,status')
        print(result)

    def test_append_jira_filter_007_success_body_is_str_no_columns(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_jira_filter(
            '核心后台公告栏', 'confluence rest api 测试', '核心后台')
        print(result)

    def test_append_jira_filter_008_success_body_is_str_has_columns(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_jira_filter(
            '核心后台公告栏', 'confluence rest api 测试', '核心后台', 'key,summary,status')
        print(result)

    def test_append_jira_filter_009_success_body_is_str_has_columns_error(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').append_confluence_jira_filter(
            '核心后台公告栏', 'confluence rest api 测试', '核心后台', 'key,summary,status,test')
        print(result)

    def test_export_confluence_page_as_pdf_001_success(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').export_confluence_page_as_pdf('核心后台公告栏', 'confluence rest api 测试',
                                                                              'D:/confluence rest api 测试.pdf')
        print(result)

    def test_export_confluence_page_as_word_001_success(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').export_confluence_page_as_word('核心后台公告栏', 'confluence rest api 测试',
                                                                               'D:/confluence rest api 测试.docx')
        print(result)

    def test_create_confluence_page_001_success(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').create_confluence_page(
            '核心后台公告栏', '陈颖', 'confluence rest api 测试', "使用confluence rest api创建的页面")
        print(result)

    def test_clean_confluence_page_001_success(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').clean_confluence_page(
            '核心后台公告栏', 'confluence rest api 测试')
        print(result)

    def test_create_confluence_page(self):
        i = 1
        while 1:
            create = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                    'Since@445481').clean_confluence_page(
                '核心后台公告栏', 'confluence rest api 测试{}'.format(i))
            print(create)
            table = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                   'Since@445481').append_confluence_table('核心后台公告栏', 'confluence rest api 测试',
                                                                           ['主机', '内存类型', '内存子类型',
                                                                            '主机内存配置大小(GB)'], [
                                                                               ['ASI391', 'MEM', 'SHM', '255'],
                                                                               ['ASI392', 'MEM', 'SHM', '255'],
                                                                               ['ASR791', 'MEM', 'SHM', '383'],
                                                                               ['ASR792', 'MEM', 'SHM', '383'],
                                                                               ['ASR793', 'MEM', 'SHM', '191'],
                                                                               ['ASR794', 'MEM', 'SHM', '191'],
                                                                               ['AST591', 'MEM', 'SHM', '383'],
                                                                               ['AST592', 'MEM', 'SHM', '383'],
                                                                               ['AST593', 'MEM', 'SHM', '383'],
                                                                               ['AST594', 'MEM', 'SHM', '383'],
                                                                               ['BST571', 'MEM', 'SHM', '128'],
                                                                               ['BST572', 'MEM', 'SHM', '128'],
                                                                               ['DSR761', 'MEM', 'SHM', '383'],
                                                                               ['DSR762', 'MEM', 'SHM', '383'],
                                                                               ['DSR763', 'MEM', 'SHM', '383'],
                                                                               ['DSR764', 'MEM', 'SHM', '191'],
                                                                               ['DST561', 'MEM', 'SHM', '383'],
                                                                               ['DST562', 'MEM', 'SHM', '383'],
                                                                               ['ESI301', 'MEM', 'SHM', '63'],
                                                                               ['ESI302', 'MEM', 'SHM', '63'],
                                                                               ['ESR701', 'MEM', 'SHM', '127'],
                                                                               ['ESR702', 'MEM', 'SHM', '127'],
                                                                               ['ESR703', 'MEM', 'SHM', '127'],
                                                                               ['EST101', 'MEM', 'SHM', '71'],
                                                                               ['EST102', 'MEM', 'SHM', '71'],
                                                                               ['EST103', 'MEM', 'SHM', '127'],
                                                                               ['HSI201', 'MEM', 'SHM', '15'],
                                                                               ['HSI202', 'MEM', 'SHM', '127'],
                                                                               ['HSI301', 'MEM', 'SHM', '191'],
                                                                               ['HSI302', 'MEM', 'SHM', '191'],
                                                                               ['HSR601', 'MEM', 'SHM', '15'],
                                                                               ['HSR602', 'MEM', 'SHM', '47'],
                                                                               ['HSR701', 'MEM', 'SHM', '383'],
                                                                               ['HSR702', 'MEM', 'SHM', '383'],
                                                                               ['HSR703', 'MEM', 'SHM', '383'],
                                                                               ['HSR704', 'MEM', 'SHM', '383'],
                                                                               ['HSR705', 'MEM', 'SHM', '383'],
                                                                               ['HSR706', 'MEM', 'SHM', '255'],
                                                                               ['HST001', 'MEM', 'SHM', '15'],
                                                                               ['HST002', 'MEM', 'SHM', '31'],
                                                                               ['HST101', 'MEM', 'SHM', '255'],
                                                                               ['HST102', 'MEM', 'SHM', '255'],
                                                                               ['HST103', 'MEM', 'SHM', '255'],
                                                                               ['HST104', 'MEM', 'SHM', '255'],
                                                                               ['HST105', 'MEM', 'SHM', '255'],
                                                                               ['HST106', 'MEM', 'SHM', '127']])
            print(table)
            image = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                   'Since@445481').append_confluence_image(
                '核心后台公告栏', 'confluence rest api 测试{}'.format(i), "D:/Lighthouse.jpg")
            print(image)
            lists = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                   'Since@445481').append_confluence_list('核心后台公告栏',
                                                                          'confluence rest api 测试{}'.format(i),
                                                                          ['ASI391,MEM,SHM,255', 'ASI392,MEM,SHM,255',
                                                                           'ASR791,MEM,SHM,383', 'ASR792,MEM,SHM,383',
                                                                           'ASR793,MEM,SHM,191', 'ASR794,MEM,SHM,191',
                                                                           'AST591,MEM,SHM,383', 'AST592,MEM,SHM,383',
                                                                           'AST593,MEM,SHM,383', 'AST594,MEM,SHM,383',
                                                                           'BST571,MEM,SHM,128', 'BST572,MEM,SHM,128',
                                                                           'DSR761,MEM,SHM,383', 'DSR762,MEM,SHM,383',
                                                                           'DSR763,MEM,SHM,383', 'DSR764,MEM,SHM,191',
                                                                           'DST561,MEM,SHM,383', 'DST562,MEM,SHM,383',
                                                                           'ESI301,MEM,SHM,63', 'ESI302,MEM,SHM,63',
                                                                           'ESR701,MEM,SHM,127', 'ESR702,MEM,SHM,127',
                                                                           'ESR703,MEM,SHM,127', 'EST101,MEM,SHM,71',
                                                                           'EST102,MEM,SHM,71', 'EST103,MEM,SHM,127',
                                                                           'HSI201,MEM,SHM,15', 'HSI202,MEM,SHM,127',
                                                                           'HSI301,MEM,SHM,191', 'HSI302,MEM,SHM,191',
                                                                           'HSR601,MEM,SHM,15', 'HSR602,MEM,SHM,47',
                                                                           'HSR701,MEM,SHM,383', 'HSR702,MEM,SHM,383',
                                                                           'HSR703,MEM,SHM,383', 'HSR704,MEM,SHM,383',
                                                                           'HSR705,MEM,SHM,383', 'HSR706,MEM,SHM,255',
                                                                           'HST001,MEM,SHM,15', 'HST002,MEM,SHM,31',
                                                                           'HST101,MEM,SHM,255', 'HST102,MEM,SHM,255',
                                                                           'HST103,MEM,SHM,255', 'HST104,MEM,SHM,255',
                                                                           'HST105,MEM,SHM,255', 'HST106,MEM,SHM,127'])
            print(lists)
            jira = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                  'Since@445481').append_confluence_jira_filter(
                '核心后台公告栏', 'confluence rest api 测试{}'.format(i), 'http://eqops.tc.com/jira/browse/JIRA-810')
            print(jira)
            jql = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                 'Since@445481').append_confluence_jira_filter(
                '核心后台公告栏', 'confluence rest api 测试{}'.format(i), 'project = JIRA服务台 AND resolution = 已完成',
                'key,summary,status')
            print(jql)
            dicts = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                   'Since@445481').append_confluence_dict('核心后台公告栏',
                                                                          'confluence rest api 测试{}'.format(i), [
                                                                              {'主机': 'ASI391', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
                                                                              {'主机': 'ASI392', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
                                                                              {'主机': 'ASR791', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'ASR792', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'ASR793', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '191'},
                                                                              {'主机': 'ASR794', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '191'},
                                                                              {'主机': 'AST591', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'AST592', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'AST593', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'AST594', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'BST571', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '128'},
                                                                              {'主机': 'BST572', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '128'},
                                                                              {'主机': 'DSR761', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'DSR762', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'DSR763', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'DSR764', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '191'},
                                                                              {'主机': 'DST561', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'DST562', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'ESI301', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '63'},
                                                                              {'主机': 'ESI302', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '63'},
                                                                              {'主机': 'ESR701', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
                                                                              {'主机': 'ESR702', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
                                                                              {'主机': 'ESR703', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
                                                                              {'主机': 'EST101', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '71'},
                                                                              {'主机': 'EST102', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '71'},
                                                                              {'主机': 'EST103', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
                                                                              {'主机': 'HSI201', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '15'},
                                                                              {'主机': 'HSI202', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
                                                                              {'主机': 'HSI301', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '191'},
                                                                              {'主机': 'HSI302', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '191'},
                                                                              {'主机': 'HSR601', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '15'},
                                                                              {'主机': 'HSR602', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '47'},
                                                                              {'主机': 'HSR701', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'HSR702', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'HSR703', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'HSR704', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'HSR705', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '383'},
                                                                              {'主机': 'HSR706', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
                                                                              {'主机': 'HST001', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '15'},
                                                                              {'主机': 'HST002', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '31'},
                                                                              {'主机': 'HST101', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
                                                                              {'主机': 'HST102', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
                                                                              {'主机': 'HST103', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
                                                                              {'主机': 'HST104', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
                                                                              {'主机': 'HST105', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '255'},
                                                                              {'主机': 'HST106', '内存类型': 'MEM',
                                                                               '内存子类型': 'SHM', '主机内存配置大小(GB)': '127'},
                                                                          ])
            print(dicts)
            i += 1
            print(i)

            if i > 30:
                break

    def test_append_confluence_page(self):
        self.test_create_confluence_page_001_success()
        self.test_append_jira_filter_001_success_body_is_url_no_columns()
        self.test_append_jira_filter_003_success_body_is_jira_id_no_columns()
        self.test_append_jira_filter_004_success_body_is_jql_has_columns()
        self.test_append_jira_filter_005_success_body_is_jql_no_columns()
        self.test_append_jira_filter_005_success_body_is_name_no_columns()
        self.test_append_jira_filter_006_success_body_is_name_has_columns()
        self.test_append_jira_filter_007_success_body_is_str_no_columns()
        self.test_append_jira_filter_008_success_body_is_str_has_columns()

    def test_create_confluence_page_002_space_not_exists(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').create_confluence_page(
            '核心后台公告', '陈颖', 'confluence rest api 测试', '使用confluence rest api创建的页面')
        print(result)

    def test_create_confluence_page_003_parent_title_not_exists(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').create_confluence_page(
            '核心后台公告栏', '陈', 'confluence rest api 测试', '使用confluence rest api创建的页面')
        print(result)

    def test_create_confluence_page_004_page_exists(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').create_confluence_page(
            '核心后台公告栏', '陈颖', 'confluence rest api 测试', '使用confluence rest api创建的页面')
        print(result)

    def test_delete_confluence_page_by_title_001_space_and_title_exist(self):
        host_env_show_2dlist = [
            "[公告]new核心后台D环境分配: HSD/HSDV",
            "[公告]new核心后台T环境分配: AST/DST/BST",
            "[公告]new核心后台R环境分配: ASR/DSR",
            "[公告]new核心后台I环境分配: ASI",
            "[公告]new核心后台T环境分配: HST-TC/HST-CC",
            "[公告]new核心后台I环境分配: HSR-TC/HSR-CC",
            "[公告]new核心后台I环境分配: HSI-TC/HSI-CC",
            "[公告]new核心后台T环境分配: EST",
            "[公告]new核心后台R环境分配: ESR",
            "[公告]new核心后台I环境分配: ESI",
            "[公告]new核心后台D环境分配: 新债券EZCSD",
            "[公告]new核心后台T环境分配: 新债券EZCST",
            "[公告]new核心后台R环境分配: 新债券EZCSR",
            "[公告]new核心后台I环境分配: 新债券EZCSI",
            "[公告]new核心后台T环境分配: CST",
            "[公告]new核心后台R环境分配: CSR",
            "[公告]new核心后台I环境分配: CSI",
            "[公告]new核心后台T环境分配: EZCST",
            "[公告]new核心后台R环境分配: EZCSR",
            "[公告]new核心后台I环境分配: EZCSI",
            "[公告]new核心后台T环境分配: EZEI&BPC",
            "[公告]new核心后台R环境分配: EZEI&BPC",
            "[公告]new核心后台I环境分配: EZEI&BPC",
            "[公告]new核心后台T环境分配: ICS",
            "[公告]new核心后台R环境分配: ICS",
            "[公告]new核心后台T环境分配: SSP",
            "[公告]new核心后台R环境分配: SSP",
            "[公告]new核心后台T环境分配: EZSR",
            "[公告]new核心后台T环境分配: 新债券RC&MC&ZC",
            "[公告]new核心后台R环境分配: 新债券RC&MC&ZC",
            "[公告]new核心后台I环境分配: 新债券RC&MC&ZC",
            "[公告]new核心后台T环境分配: 新债券EI&BPC",
            "[公告]new核心后台R环境分配: 新债券EI&BPC",
            "[公告]new核心后台I环境分配: 新债券EI&BPC",
        ]
        for value in host_env_show_2dlist:
            result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                    'Since@445481').delete_confluence_page_by_title(
                '核心后台公告栏', '{}'.format(value))
            print(result)

    def test_delete_confluence_page_by_title_002_space_not_exist(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').delete_confluence_page_by_title(
            '核心后台公告', 'confluence rest api 测试')
        print(result)

    def test_delete_confluence_page_by_title_003_title_not_exist(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').delete_confluence_page_by_title(
            '核心后台公告栏', 'confluence rest api 测')
        print(result)

    def test_get_confluence_page_url_by_title_001_space_and_title_exist(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').get_confluence_page_url_by_title(
            '核心后台公告栏', '陈颖')
        print(result)

    def test_get_confluence_page_url_by_title_002_space_not_exist(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').get_confluence_page_url_by_title(
            '核心后台公告', '陈颖')
        print(result)

    def test_get_confluence_page_url_by_title_004_title_not_exist(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').get_confluence_page_url_by_title(
            '核心后台公告栏', 'chenying')
        print(result)

    def test_delete_confluence_page_by_url_001_page_exists(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').delete_confluence_page_by_url(
            'http://eqops.tc.com/confluence/pages/viewpage.action?pageId=43998938')
        print(result)

    def test_delete_confluence_page_by_url_002_page_not_exists(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').delete_confluence_page_by_url(
            'http://eqops.tc.com/confluence/pages/viewpage.action?pageId=43985869')
        print(result)

    def test_get_confluence_page_title_by_url_001_page_exists(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').get_confluence_page_title_by_url(
            'http://eqops.tc.com/confluence/pages/viewpage.action?pageId=43990360')
        print(result)

    def test_get_confluence_page_title_by_url_002_page_not_exists(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').get_confluence_page_title_by_url(
            'http://eqops.tc.com/confluence/pages/viewpage.action?pageId=43985869')
        print(result)

    def test_get_confluence_user_details_by_username_002_fail_username__not_exists(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').get_confluence_user_details_by_username("chenyin")
        print(result)

    def test_get_confluence_all_groups(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').get_confluence_all_groups()
        print(result)

    def test_get_confluence_group_members(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').get_confluence_group_members("ambuild_intergration")
        print(result)

    def test_get_confluence_group_members_name(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').get_confluence_group_members_name(
            ['bhou', 'cxhou', 'cxiao', 'dltan', 'dnshi', 'dsheng', 'ffan', 'fmpi', 'frtang', 'gwhu', 'henghuang', 'hhe',
             'hlfang', 'hlliu', 'hongyanchen', 'hren', 'huanhuanchen', 'hxzhuo', 'jchuang', 'jdu', 'jiajunwu', 'jili',
             'jli', 'jlzhang', 'jqmin', 'jrli', 'junzhang', 'jwang2', 'jwwen', 'kkyue', 'ksong', 'lfyang', 'lilizhang',
             'llzhai', 'lthe', 'lwguan', 'lzhou', 'mcheng', 'mhwang', 'mliu2', 'mmyang', 'msha', 'mzhang', 'pgui',
             'qianwu2', 'qqjiang', 'ruiruiwang', 'rzzhou', 'shzhang', 'spwu', 'stwang', 'suzhang', 'sxzhang', 'syshen',
             'ttli', 'tyzhang', 'wmzhang', 'wyshi', 'xilinlin', 'xinwu', 'xqzhou', 'xxguan', 'xzguo', 'yanchen',
             'yangli', 'yangyangwang', 'yeyan', 'yfu', 'ygong', 'yingzhang', 'yizhang', 'yjshi', 'yjwang', 'yliu',
             'ynfeng', 'yongjianzhang', 'ytian', 'yuanzhang2', 'ywzhao', 'yxliu', 'yyuan', 'zcchen', 'zdtu', 'zhlin',
             'zjxu', 'zjzhang', 'zma', 'zqxu', 'zzhan', 'zzliu'])
        print(result)

    def test_get_confluence_all_group_members(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').get_confluence_all_members()
        print(result)

    def test_get_confluence_user_details_by_username_001_success_username_exists(self):
        result = ConfluenceUtil('http://eqops.tc.com/confluence', 'chenying',
                                'Since@445481').get_confluence_user_details_by_username("chenying")
        print(result)
