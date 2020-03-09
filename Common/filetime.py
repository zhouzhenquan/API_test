'''
 @Time    : 2020/2/24 13:18
 @Author  : 周振全
 @File    : filetime.py
 @Software: PyCharm

'''
"""封装文件名+时间"""


import time


class File_time_(object):
    def time(self):
        return time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime(time.time()))

File_time = File_time_()

