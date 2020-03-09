"""
============================
Author:周振全
Time:2020/2/23 6:35 下午
E-mail:17764509133@163.com
============================
"""
import random
def iphone():
    phone = '138'
    for i in range(8):
        n = random.randint(1,9)
        phone += str(n)
    return phone

def iphone_1():
    phone = '177'
    n = random.randint(100000000,900000000)
    phone += str(n)[1::]
    return phone

res = iphone()
res1 = iphone_1()
print(res)
print(res1)
