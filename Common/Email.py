"""
-- coding: utf-8 --
@Time : 2020/3/16 13:19
@Author : 周振全
@Site : 
@File : Email.py
@Software: PyCharm

"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from Common.config import conf


def send_email(filename,title):

    # 连接邮箱的smtp服务器，并登录
    smtp = smtplib.SMTP_SSL(host=conf.get("email",'host'),port=conf.getint("email",'port'))
    smtp.login(user=conf.get("email",'user'),password=conf.get("email",'password'))

    # 构建一封邮箱
    msg = MIMEMultipart()

    with open(filename,"rb") as F:
        content = F.read()

    # 创建邮文本内容
    test_msg = MIMEText(content,_subtype="html",_charset='utf-8')
    # 添加到多组邮件的附件中
    msg.attach(test_msg)

    # 创建邮件附件
    report_file = MIMEApplication(content)
    report_file.add_header('content-disposition', 'attachment', filename=os.path.split(filename)[-1])
    # 将附件添加到多组件的邮件中
    msg.attach(report_file)


    # 主题
    msg["Subject"] = title
    # 发件人
    msg["From"] = conf.get("email",'from_adder')
    # 收件人
    msg["To"] = conf.get("email",'to_adder')

    # 发送邮箱
    smtp.send_message(msg,from_addr=conf.get("email",'from_adder'),to_addrs=conf.get("email",'to_adder'))











