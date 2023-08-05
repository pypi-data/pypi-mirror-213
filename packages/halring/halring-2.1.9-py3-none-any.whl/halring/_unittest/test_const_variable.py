# coding=utf-8
import unittest
from halring.common.halring_const_variable import ConstVariable


class TestConstVariableUtil(unittest.TestCase):

    def test_const_variable_001(self):
        print(ConstVariable.NO_CHECK)
        print(ConstVariable.CHECK_CONSISTENCY)
        print(ConstVariable.CHECK_STEP)
        print(ConstVariable.SPACE)
        print(ConstVariable.EMPTY)
        print(ConstVariable.STEP_AUTOLEN)
        print(ConstVariable.STEP_NULL)
        print(ConstVariable.SEARCH_NOT_EXIST)
        print(ConstVariable.VMS_SPECIAL)
