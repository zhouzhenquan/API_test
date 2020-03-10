'''
 @Time    : 2020/2/25 19:41
 @Author  : 周振全
 @File    : test_recharge.py
 @Software: PyCharm

'''

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
from decimal import Decimal
from Common.handle_data import Case_Data,replace_data

case_file = os.path.join(DATADIR, 'apicases.xlsx')


@ddt
class Test_Recharge(unittest.TestCase):
    excel = operation_excel(case_file, 'recharge')
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
    def test_recharge(self, case):
        # 准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case['method']

        # 替换用户id
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])

        headers = eval(conf.get('env', 'headers'))
        headers["Authorization"] = getattr(Case_Data,"token_value")

        # 预期结果
        expected = eval(case['expected'])
        row = case['case_id'] + 1

        # 发送请求前获取用户
        if case["check_sql"]:
            sql = 'SELECT leave_amount FROM futureloan.member where mobile_phone={}'.format(
                conf.get('test_data', 'phone'))
            start_money = self.db.find_one(sql)['leave_amount']

        # 发送请求获取结果
        response = self.request.send_requests_sc(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 发送请求后获取用户
        if case["check_sql"]:
            sql = 'SELECT leave_amount FROM futureloan.member where mobile_phone={}'.format(
                conf.get('test_data', 'phone'))
            end_money = self.db.find_one(sql)['leave_amount']

        # 断言比对预期结果和实际结果
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])

            # 判断是否需要进行判断
            if case['check_sql']:
                self.assertEqual(end_money - start_money, Decimal(str(data['amount'])))


        except AssertionError as e:
            self.excel.write_excel(row=row, column=8, value='未通过')
            log.error('用例：{}，执行'.format(case['title']) + color.white_red('未通过'))
            raise e
        else:
            self.excel.write_excel(row=row, column=8, value='通过')
            log.info('用例：{}，执行'.format(case['title']) + color.white_green('通过'))
