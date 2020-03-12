"""
-- coding: utf-8 --
@Time : 2020/3/11 20:36
@Author : 周振全
@Site : 
@File : test_info.py
@Software: PyCharm

"""

import unittest
import os
import jsonpath
from Library.ddt import ddt, data
from Common.Excel import operation_excel
from Common.Path import DATADIR
from Common.config import conf
from Common.request_1 import SendRequests
from Common.Login import log
from Common.Colour import color
from Common.Connect_DB import DB
from Common.handle_data import Case_Data,replace_data

case_file = os.path.join(DATADIR, 'apicases.xlsx')


@ddt
class Test_Info(unittest.TestCase):
    excel = operation_excel(case_file, 'info')
    cases = excel.read_excel()
    request = SendRequests()
    db = DB()

    @classmethod
    def setUpClass(cls):
        # 准备登录的数据
        # 获取登录的URL地址
        url = conf.get("env", "url") + "/member/login"
        # 从配置表中读取登录账号和密码
        data = {
            "mobile_phone": conf.get("test_data", "phone"),
            "pwd": conf.get("test_data", "pwd")
        }
        # 请求头
        headers = eval(conf.get("env", "headers"))
        # 发送请求进行登录
        response = cls.request.send_requests_sc(url=url, method="post", json=data, headers=headers)
        # 获取返回的数据
        res = response.json()
        # 提取token()
        token = jsonpath.jsonpath(res, "$..token")[0]
        token_type = jsonpath.jsonpath(res, "$..token_type")[0]
        # 将提取到的token设置为类属性
        Case_Data.token_value = token_type + " " + token
        # 提取用户的登录id，保存为类属性
        Case_Data.member_id = str(jsonpath.jsonpath(res, "$..id")[0])

    @data(*cases)
    def test_info(self, case):
        # 准备用例数据
        url = conf.get("env", "url") + replace_data(case["url"])
        method = case['method']


        headers = eval(conf.get('env', 'headers'))
        headers["Authorization"] = getattr(Case_Data,"token_value")

        # 预期结果
        expected = eval(case['expected'])
        row = case['case_id'] + 1


        # 发送请求获取结果
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










