"""
-- coding: utf-8 --
@Time : 2020/3/11 21:11
@Author : 周振全
@Site : 
@File : test_loans.py
@Software: PyCharm

"""
import os
import unittest
from Common.Excel import operation_excel
from Common.Path import DATADIR
from Library.ddt import ddt, data
from Common.config import conf
from Common.handle_data import replace_data
from Common.request_1 import SendRequests
from Common.Login import log
from Common.Colour import color

case_file = os.path.join(DATADIR, "apicases.xlsx")


@ddt
class Test_Loans(unittest.TestCase):
    excel = operation_excel(case_file, "loans")
    cases = excel.read_excel()
    request = SendRequests()
    @data(*cases)
    def test_loans(self, case):
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        data = replace_data(case['data'])
        headers = eval(conf.get("env", "headers"))
        expected = eval(case['expected'])
        row = case['case_id'] + 1

        response = self.request.send_requests_sc(url=url,method=method,params=data,headers=headers)
        res = response.json()

        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
        except AssertionError as e:
            self.excel.write_excel(row=row, column=8, value='未通过')
            log.error('用例：{}，执行'.format(case['title']) + color.white_red('未通过'))
            raise e
        else:
            self.excel.write_excel(row=row, column=8, value='通过')
            log.info('用例：{}，执行'.format(case['title']) + color.white_green('通过'))