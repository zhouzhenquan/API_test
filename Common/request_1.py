"""
============================
Author:周振全
Time:2020/2/23 5:36 下午
E-mail:17764509133@163.com
============================
"""
import requests
class SendRequests(object):

    def __init__(self):
        self.session = requests.session()


    def send_requests_sc(self, url, method, headers=None, params=None, data=None, json=None, files=None):
        # 字母转换大小写
        method = method.lower()
        if method == "get":
            response = self.session.get(url=url, params=params, headers=headers)
        elif method == "post":
            response = self.session.post(url=url, data=data, json=json, files=files, headers=headers)
        elif method == "patch":
            response = self.session.patch(url=url, data=data, json=json, files=files, headers=headers)

        return response
