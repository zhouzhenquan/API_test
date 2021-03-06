"""
============================
Author:周振全
Time:2020/2/14 8:09 下午
E-mail:17764509133@163.com
============================
"""
import os
import unittest
from Library.HTMLTestRunnerNew import HTMLTestRunner
from Common.Path import CASEDIR, REPORTDIR
from Common.filetime import File_time
from BeautifulReport import BeautifulReport
from Test_Case import test_Main
from Common.Email import send_email

suite = unittest.TestSuite()
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASEDIR))

# suite = unittest.defaultTestLoader.loadTestsFromModule(test_Main)
# file_path = os.path.join(REPORTDIR, File_time.time() + 'report.html')
# runner = HTMLTestRunner(stream=open(file_path, 'wb'),
#                         title="Python报告",
#                         description="登录测试",
#                         tester="周振全")
# runner.run(suite)
# send_email(file_path,"Python_24报告")

br = BeautifulReport(suite)
br.report("前程贷用例",filename=File_time.time() + 'report.html',report_dir=REPORTDIR)
