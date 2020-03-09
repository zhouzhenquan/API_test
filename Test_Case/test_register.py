"""
============================
Author:周振全
Time:2020/2/23 5:40 下午
E-mail:17764509133@163.com
============================
"""
import random
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



case_file = os.path.join(DATADIR, 'apicases.xlsx')

"""注册"""
@ddt
class Test_register(unittest.TestCase):
    excel = operation_excel(case_file, 'register')
    cases = excel.read_excel()
    request = SendRequests()
    db = DB()

    @data(*cases)
    def test_register(self, case):
        # 准备用例数据
        url = conf.get("env", "url") + case['url']
        method = case['method']
        # 替换手机号码
        phone = self.iphone()
        case['data'] = case['data'].replace('#phone#', phone)

        data = eval(case["data"])
        headers = eval(conf.get('env', 'headers'))
        # 预期结果
        expected = eval(case['expected'])
        row = case['case_id'] + 1

        # 发送请求获取结果
        response = self.request.send_requests_sc(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 注册后，进行数据库校验
        if case["check_sql"]:
            sql = 'select * from futureloan.member where mobile_phone = {}'.format(data['mobile_phone'])
            count = self.db.find_count(sql)
            self.assertEqual(1,count)


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

    # 手机号码
    def iphone(self):
        phone = '138'
        for i in range(8):
            n = random.randint(1, 9)
            phone += str(n)
        return phone


"""登录"""
@ddt
class Test_login(unittest.TestCase):
    excel = operation_excel(case_file, 'login')
    cases = excel.read_excel()
    request = SendRequests()

    @data(*cases)
    def test_login(self, case):
        # 准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case['method']

        data = eval(case["data"])
        headers = eval(conf.get('env', 'headers'))
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
