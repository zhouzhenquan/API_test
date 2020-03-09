"""
============================
Author:周振全
Time:2020/2/15 5:55 下午
E-mail:17764509133@163.com
============================
"""

import os

# # 当前文件绝对路径
# res = os.path.abspath(__file__)
# print(res)
#
# # 指定文件父级目录
# res1 = os.path.dirname(res)
# print(res1)
#
# res2 = os.path.dirname(res1)
# print(res2)

# 项目目录路径
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASEDIR)
# 测试模块目录
CASEDIR = os.path.join(BASEDIR,"Test_Case")
# print(CASEDIR)
# 测试数据目录
DATADIR = os.path.join(BASEDIR,'Data')
# print(DATADIR)
# 测试报告目录
REPORTDIR = os.path.join(BASEDIR,'Reports')
# print(REPORTDIR)
# 配置文件目录
CONFDIR= os.path.join(BASEDIR,'Config')
# print(CONFDIR)
# 日志文件目录
LOGDIR = os.path.join(BASEDIR,'Log')
# print(LOGDIR)