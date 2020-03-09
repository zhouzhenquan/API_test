"""
============================
Author:周振全
Time:2020/2/12 9:31 下午
E-mail:17764509133@163.com
============================
"""
import os
import logging
from Common.config import conf
from Common.Path import LOGDIR


class My_Log(object):

    @staticmethod
    def My_log():
        # 创建收集器
        mylog = logging.getLogger('zzq')
        mylog.setLevel(conf.get('log', 'level'))

        # 控制台
        sh = logging.StreamHandler()
        sh.setLevel(conf.get('log', 'sh_level'))
        mylog.addHandler(sh)

        # 文件
        fh = logging.FileHandler(filename=os.path.join(LOGDIR, "log.log"), encoding='utf-8')
        fh.setLevel(conf.get('log', 'fh_level'))
        mylog.addHandler(fh)

        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s-%(name)s-日志信息：%(message)s')
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)

        return mylog


log = My_Log.My_log()
