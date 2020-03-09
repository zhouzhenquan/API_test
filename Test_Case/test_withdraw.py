'''
 @Time    : 2020/2/28 14:41
 @Author  : 周振全
 @File    : test_withdraw.py
 @Software: PyCharm

'''

import os
import unittest
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

file_path = os.path.join(DATADIR, "apicases.xlsx")


@ddt
class Test_Withdraw(unittest.TestCase):
    excel = operation_excel(file_path, 'withdraw')
    cases = excel.read_excel()
    request = SendRequests()
    db = DB()

    @data(*cases)
    def test_withdraw(self, case):
        url = conf.get('env', 'url') + case['url']
        case["data"] = case['data'].replace("#phone#", conf.get('test_data', 'phone'))
        case["data"] = case['data'].replace("#pwd#", conf.get('test_data', 'pwd'))
        headers = eval(conf.get('env', 'headers'))

        # 是否是取现接口 如果是就加上请求头
        if case['interface'].lower() == "withdraw":
            headers["Authorization"] = self.token_value
            case["data"] = case['data'].replace("#member_id#", str(self.member_id))

        data = eval(case['data'])
        expected = eval(case["expected"])
        method = case['method']
        row = case["case_id"] + 1

        # 判断是否需要进行sql检验
        if case["check_sql"] :
            sql = case["check_sql"].format(conf.get("test_data","phone"))
            start_money = self.db.find_one(sql)["leave_amount"]

        response = self.request.send_requests_sc(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 是否是登录接口 如果是就获取token
        if case['interface'].lower() == 'login':
            # 提取用户ID保存为类属性
            Test_Withdraw.member_id = jsonpath.jsonpath(res, '$..id')[0]
            token = jsonpath.jsonpath(res, '$..token')[0]
            token_type = jsonpath.jsonpath(res, '$..token_type')[0]
            # 提取token保存类属性
            Test_Withdraw.token_value = token_type + " " + token

        # 断言  比对预期结果和实际结果
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            # 判断是否需要进行sql检验
            if case["check_sql"]:
                sql = case["check_sql"].format(conf.get("test_data","phone"))
                end_money = self.db.find_one(sql)["leave_amount"]
                # 比对取现金额是否正确
                self.assertEqual(Decimal(str(data["amount"])),start_money-end_money)

        except AssertionError as e:
            print("预期结果：",expected)
            print("实际结果：",res)

            self.excel.write_excel(row=row, column=8, value='未通过')
            log.error('用例：{}，执行'.format(case['title']) + color.white_red('未通过'))
            raise e
        else:
            self.excel.write_excel(row=row, column=8, value='通过')
            log.info('用例：{}，执行'.format(case['title']) + color.white_green('通过'))
