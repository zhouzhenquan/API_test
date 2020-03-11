"""
-- coding: utf-8 --
@Time : 2020/3/10 20:32
@Author : 周振全
@Site : 
@File : test_audit.py
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
from Common.handle_data import Case_Data, replace_data
from Common.Connect_DB import DB
"""
审核步骤：
    1. 登录，所有的审核用例都要执行登录操作
    2. 加标，每一个用例执行之前都要加标
    3. 审核，

"""

file_path = os.path.join(DATADIR, 'apicases.xlsx')

"""登录"""


@ddt
class Test_Audit(unittest.TestCase):
    excel = operation_excel(file_path, 'audit')
    cases = excel.read_excel()
    request = SendRequests()
    db = DB()
    @classmethod
    def setUpClass(cls):
        """所有的用例执行前都要执行一次"""
        # 准备登录的数据
        # 获取登录的URL地址
        url = conf.get("env", "url") + "/member/login"
        # 从配置表中读取登录账号和密码
        data = {
            "mobile_phone": conf.get("test_data", "admin_phone"),
            "pwd": conf.get("test_data", "admin_pwd")
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
        Case_Data.admin_token_value = token_type + " " + token
        # 提取用户的登录id，保存为类属性
        Case_Data.admin_member_id = str(jsonpath.jsonpath(res, "$..id")[0])

    def setUp(self):
        """每个用例之前都要执行"""
        """添加加标"""
        url = conf.get("env", "url") + "/loan/add"
        headers = eval(conf.get('env', 'headers'))
        headers["Authorization"] = getattr(Case_Data, "admin_token_value")
        data = {
            "member_id": getattr(Case_Data,"admin_member_id"),
             "title":"借钱实现财富自由",
             "amount":2000,
             "loan_rate":12.0,
             "loan_term":3,
             "loan_date_type":1,
             "bidding_days":5
                }
        # 发送请求
        response = self.request.send_requests_sc(url=url, method="post", json=data, headers=headers)
        res = response.json()

        # 提取审核需要用到的项目ID
        Case_Data.loan_id = str(jsonpath.jsonpath(res, "$..id")[0])

    @data(*cases)
    def test_audit(self, case):
        # 准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case['method']

        case["data"] = replace_data(case["data"])

        data = eval(case["data"])
        headers = eval(conf.get('env', 'headers'))
        headers["Authorization"] = getattr(Case_Data, "admin_token_value")

        # 预期结果
        expected = eval(case['expected'])
        row = case['case_id'] + 1

        # 发送请求获取结果
        response = self.request.send_requests_sc(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 判断是否是审核通过的用例,并且审核通过
        if expected["code"] == 0 and case["title"] == "审核通过":
            Case_Data.pass_loan_id = str(data["loan_id"])

        # 断言比对预期结果和实际结果
        try:
            self.assertEqual(expected['code'], res['code'])
            self.assertEqual(expected['msg'], res['msg'])
            # 判断是否进行数据库校验
            if case["check_sql"]:
                sql = replace_data(case["check_sql"])
                status = self.db.find_one(sql)["status"]
                # 断言数据库中标的状态是否与预期一致
                self.assertEqual(expected['status'],status)


        except AssertionError as e:
            self.excel.write_excel(row=row, column=8, value='未通过')
            log.error('用例：{}，执行'.format(case['title']) + color.white_red('未通过'))
            raise e
        else:
            self.excel.write_excel(row=row, column=8, value='通过')
            log.info('用例：{}，执行'.format(case['title']) + color.white_green('通过'))
