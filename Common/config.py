"""
============================
Author:周振全
Time:2020/2/12 11:42 上午
E-mail:17764509133@163.com
============================
"""
"""
封装的需求：

1、简化创建配置文件解析器对象，加载配置文件的流程（需要封装），提示（重写init方法）
2、读取数据（不进行封装，使用原来的方法），通过继承父类即可
3、简化写入数据的操作（需要封装），提示：自定义一个write_data方法。

"""
import os
from configparser import ConfigParser
from Common.Path import CONFDIR

class config(ConfigParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.read(filename,encoding='utf-8')

    def write_data(self, section, option, content):
        self.set(section, option, content)
        self.write(fp=open(self.filename, "w"))



conf = config(os.path.join(CONFDIR,'config.ini'))

