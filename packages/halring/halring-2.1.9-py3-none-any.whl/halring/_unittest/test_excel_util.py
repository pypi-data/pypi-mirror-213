# -*- coding:UTF-8 -*-
import unittest
from halring.excel.halring_excel import ExcelUtil


class TestExcelUtil(unittest.TestCase):
    def test_excel_util_001(self):
        xlsxutil = ExcelUtil("test_xls.xls")
        value = xlsxutil.read_excel_to_dict()
        print(value)

    def test_excel_util_002(self):
        xlsxutil = ExcelUtil("test_xlsx.xlsx")
        value = xlsxutil.read_excel_to_dict()
        print(value)

    def test_excel_util_003(self):
        xlsxutil = ExcelUtil("test_xls.xls")
        webbook = xlsxutil.write_cell(1, 1, 'test')

    def test_excel_util_004(self):
        xlsxutil = ExcelUtil("test_xlsx.xlsx")
        webbook = xlsxutil.write_cell(1, 1, 'test')
        print(webbook)

    def test_excel_util_readHead(self):
        xlsxutil = ExcelUtil("test_xls.xls")
        data = xlsxutil.readHead()
        print(data)

    def test_excel_util_readrow(self):
        xlsxutil = ExcelUtil("test_xls.xls")
        data = xlsxutil.readRow(1)
        print(data)

    def test_excel_util_dict_to_excel(self):
        xlsxutil = ExcelUtil('s')
        xlsxutil.dict_to_excel({"ID": [1, 2, 3], "Name": ["Tim", "ZhangSan", "LiSi"]}, "./test_generate.xlsx")
        print("ok")
