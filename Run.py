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

suite = unittest.TestSuite()
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASEDIR))

file_path = os.path.join(REPORTDIR, File_time.time() + 'report.html')

runner = HTMLTestRunner(stream=open(file_path, 'wb'),
                        title="Python报告",
                        description="登录测试",
                        tester="周振全")
runner.run(suite)
