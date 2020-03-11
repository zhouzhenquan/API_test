"""
-- coding: utf-8 --
@Time : 2020/3/10 18:57
@Author : 周振全
@Site : 
@File : test_add.py
@Software: PyCharm

"""
import jsonpath
import unittest
import os
from Common.Excel import operation_excel
from Common.Path import DATADIR
from Library.ddt import ddt,data
from Common.config import conf
from Common.request_1 import SendRequests
from Common.handle_data import Case_Data,replace_data
from Common.Login import log
from Common.Colour import color


file_name = os.path.join(DATADIR,'apicases.xlsx')

@ddt
class Test_add(unittest.TestCase):
    excel = operation_excel(file_name,'add')
    cases = excel.read_excel()
    request = SendRequests()

    @classmethod
    def setUp(cls):
        """登录管理员账号"""

        url = conf.get("env","url") + "/member/login"
        data = {
            "mobile_phone":conf.get("test_data","admin_phone"),
            "pwd":conf.get("test_data","admin_pwd")
        }
        # 请求头
        headers = eval(conf.get("env","headers"))
        response = cls.request.send_requests_sc(url=url,method="post",json=data,headers=headers)
        res = response.json()
        token = jsonpath.jsonpath(res,"$..token")[0]
        token_type = jsonpath.jsonpath(res,"$..token_type")[0]
        member_id = str(jsonpath.jsonpath(res,"$..id")[0])

        # 将提取的数据保存到Case_data属性中
        Case_Data.admin_token_value = token_type + " " + token
        Case_Data.admin_member_id = member_id


    @data(*cases)
    def test_add(self,case):

        # 准备数据
        url = conf.get("env", "url") + case["url"]
        headers = eval(conf.get("env","headers"))
        headers["Authorization"] = getattr(Case_Data, "admin_token_value")
        data = eval(replace_data(case["data"]))
        expected =eval(case["expected"])
        method = case["method"]
        row = case["case_id"] + 1

        # 发送请求
        response = self.request.send_requests_sc(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 断言结果
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








        pass

