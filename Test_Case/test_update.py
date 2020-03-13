"""
-- coding: utf-8 --
@Time : 2020/3/12 21:10
@Author : 周振全
@Site : 
@File : test_update.py
@Software: PyCharm

"""
import os
import unittest
import jsonpath
from Common.Path import DATADIR
from Common.Excel import operation_excel
from Common.config import conf
from Library.ddt import data,ddt
from Common.request_1 import SendRequests
from Common.Login import log
from Common.Colour import color
from Common.handle_data import Case_Data,replace_data


case_file = os.path.join(DATADIR,"apicases.xlsx")

@ddt
class Test_Update(unittest.TestCase):
    excel = operation_excel(case_file,"update")
    cases = excel.read_excel()
    request = SendRequests()

    @classmethod
    def setUpClass(cls):
        url = conf.get('env','url') + "/member/login"
        data = {
            "mobile_phone": conf.get("test_data", "phone"),
            "pwd": conf.get("test_data", "pwd")
        }

        headers = eval(conf.get("env", "headers"))
        response = cls.request.send_requests_sc(url=url, method="post", json=data, headers=headers)
        res = response.json()

        token = jsonpath.jsonpath(res,"$..token")[0]
        token_type = jsonpath.jsonpath(res,"$..token_type")[0]
        Case_Data.token_value = token_type + " " + token
        Case_Data.member_id = str(jsonpath.jsonpath(res,"$..id")[0])


    @data(*cases)
    def test_update(self,case):

        url = conf.get('env','url') + case["url"]
        method =case['method']

        data = eval(replace_data(case["data"]))

        headers =eval(conf.get('env','headers'))
        headers["Authorization"] = getattr(Case_Data, "token_value")

        expected = eval(case['expected'])
        row = case['case_id'] + 1

        response = self.request.send_requests_sc(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 断言比对预期结果和实际结果
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












