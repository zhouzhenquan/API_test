"""
-- coding: utf-8 --
@Time : 2020/3/10 16:34
@Author : 周振全
@Site : 
@File : handle_data.py
@Software: PyCharm

"""
from Common.config import conf
import re


class Case_Data():
    """专门保存，执行过程中提取出来给其他用例的数据去使用"""
    pass


def replace_data(s):
    r1 = r"#(.+?)#"
    while re.search(r1, s):
        res = re.search(r1, s)
        data = res.group()
        key = res.group(1)
        try:
            s = s.replace(data, conf.get("test_data", key))
        except Exception:
            s = s.replace(data, getattr(Case_Data, key))
    return s
