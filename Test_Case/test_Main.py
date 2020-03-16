"""
-- coding: utf-8 --
@Time : 2020/3/11 10:50
@Author : 周振全
@Site : 
@File : test_invest.py
@Software: PyCharm

"""
import random
import jsonpath
import unittest
import os
from Library.ddt import ddt, data
from Common.Excel import operation_excel
from Common.Path import DATADIR
from Common.config import conf
from Common.request_1 import SendRequests
from Common.Login import log
from Common.Colour import color
from Common.Connect_DB import DB
from Common.handle_data import replace_data,Case_Data



case_file = os.path.join(DATADIR, 'apicases.xlsx')



"""登录"""
@ddt
class Test_Main(unittest.TestCase):
    excel = operation_excel(case_file, 'main_stream')
    cases = excel.read_excel()
    request = SendRequests()

    @data(*cases)
    def test_main(self, case):
        # 准备用例数据
        url = conf.get("env", "url") + replace_data(case["url"])
        method = case['method']
        if case["interface"] == "register":
            Case_Data.mobilephone = self.random_phone()

        data = eval(replace_data(case["data"]))
        headers = eval(conf.get('env', 'headers'))

        # 判断当前接口是不是 注册和登录，加token
        if case["interface"] != "login" and case["interface"] != "register":
            headers["Authorization"] = getattr(Case_Data,"token_value")


        # 预期结果
        expected = eval(case['expected'])
        row = case['case_id'] + 1

        # 发送请求获取结果
        response = self.request.send_requests_sc(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 判断发送请求之后，判断是不是登录，提取token
        if case["interface"].lower() == "login":
            Case_Data.member_id = str(jsonpath.jsonpath(res, '$..id')[0])
            token = jsonpath.jsonpath(res, '$..token')[0]
            token_type = jsonpath.jsonpath(res, '$..token_type')[0]
            # 提取token保存类属性
            Case_Data.token_value = token_type + " " + token


        if case["interface"] == "add":
            Case_Data.loan_id = str(jsonpath.jsonpath(res,"$..id")[0])



        # 断言比对预期结果和实际结果
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertIn(expected["msg"],res["msg"])

        except AssertionError as e:
            self.excel.write_excel(row=row, column=8, value='未通过')
            log.error('用例：{}，执行'.format(case['title']) + color.white_red('未通过'))
            raise e
        else:
            self.excel.write_excel(row=row, column=8, value='通过')
            log.info('用例：{}，执行'.format(case['title']) + color.white_green('通过'))
    def random_phone(self):
        phone = "138"
        N = random.randint(100000000,999999999)
        phone += str(N)[1:]
        return phone