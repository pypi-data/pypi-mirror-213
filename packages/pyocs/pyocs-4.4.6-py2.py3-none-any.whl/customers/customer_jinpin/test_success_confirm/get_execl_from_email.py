#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import smtplib
import time
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import poplib
import email
import datetime
import time
from email.parser import Parser
from email.header import decode_header
import traceback
import sys
import telnetlib

from customers.customer_jinpin.test_success_confirm import checkout_engineer
from pyocs import pyocs_login


class get_execl_from_email:
    logger = logging.getLogger(__name__)
    def __init__(self):
        self.logger.setLevel(level=logging.WARNING)  # 控制打印级别

    account = pyocs_login.PyocsLogin().get_account_from_json_file()
    from_addr = str(account['Username']) + "@cvte.com"
    password = account['Password']
    smtp_server = 'smtp.exmail.qq.com'

    def _format_addr(slef,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))



    def decode_str(str_in):
        value, charset = decode_header(str_in)[0]
        if charset:
            value = value.decode(charset)
        return value


    # 解析邮件,获取附件
    @staticmethod
    def get_att(msg_in, str_day_in):
        # import email
        attachment_files = []
        for part in msg_in.walk():
            # 获取附件名称类型
            file_name = part.get_filename()
            # contType = part.get_content_type()
            if file_name:
                h = email.header.Header(file_name)
                # 对附件名称进行解码
                dh = email.header.decode_header(h)
                filename = dh[0][0]
                if dh[0][1]:
                    # 将附件名称可读化
                    filename = c_step4_get_email.decode_str(str(filename, dh[0][1]))
                    print(filename)
                    # filename = filename.encode("utf-8")
                # 下载附件
                data = part.get_payload(decode=True)
                # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
                att_file = open('E:\\load_bi\\' + str_day_in + '\\' + filename, 'wb')
                attachment_files.append(filename)
                att_file.write(data)  # 保存附件
                att_file.close()
        return attachment_files

    def send_email_to_engineer(slef,toengineer,text_str):
        msg = MIMEText(text_str, 'plain', 'utf-8')  # text_str发送正文，固定语句+确认不通过的订单信息
        msg['From'] =slef._format_addr('CVTE_林祥纳<%s>' % slef.from_addr)
        msg['To'] = ';'.join(toengineer)#以逗号形式连接起来 #_format_addr('管理员 <%s>' % to_addr)#可以采用把列表分开来的方法，一个一个发

        unpassed_str="脚本自动确认不通过的订单提醒"
        sys_time=time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
        subject_str=unpassed_str+sys_time
        msg['Subject'] = Header(subject_str, 'utf-8').encode()#subject_str发送主题内容
        #主题格式，时间+“确认不通过的订单提醒”

        server = smtplib.SMTP(slef.smtp_server, 25)
        server.set_debuglevel(1)
        server.login(slef.from_addr, slef.password)
        server.sendmail(slef.from_addr, toengineer, msg.as_string())
        server.quit()



    def run_ing():
        # 输入邮件地址, 口令和POP3服务器地址:
        email_user = '******@163.com'
        # 此处密码是授权码,用于登录第三方邮件客户端
        password = '******'
        pop3_server = 'pop.163.com'
        # 日期赋值
        day = datetime.date.today()
        str_day = str(day).replace('-', '')
        print(str_day)
        # 连接到POP3服务器,有些邮箱服务器需要ssl加密，可以使用poplib.POP3_SSL
        try:
            telnetlib.Telnet(pop3_server, 995)
            server = poplib.POP3_SSL(pop3_server, 995, timeout=10)
        except:
            time.sleep(5)
            server = poplib.POP3(pop3_server, 110, timeout=10)
        # server = poplib.POP3(pop3_server, 110, timeout=120)
        # 可以打开或关闭调试信息
        # server.set_debuglevel(1)
        # 打印POP3服务器的欢迎文字:
        print(server.getwelcome().decode('utf-8'))
        # 身份认证:
        server.user(email_user)
        server.pass_(password)
        # 返回邮件数量和占用空间:
        print('Messages: %s. Size: %s' % server.stat())
        # list()返回所有邮件的编号:
        resp, mails, octets = server.list()
        # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
        print(mails)
        index = len(mails)
        # 倒序遍历邮件
        # for i in range(index, 0, -1):
        # 顺序遍历邮件
        #for i in range(1, index+1):
        for i in range(index, 0, -1):
            resp, lines, octets = server.retr(i)
            # lines存储了邮件的原始文本的每一行,
            # 邮件的原始文本:
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            # 解析邮件:
            msg = Parser().parsestr(msg_content)
            # 获取邮件时间,格式化收件时间
            date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')
            # 邮件时间格式转换
            date2 = time.strftime("%Y%m%d", date1)
            if date2 < str_day:
                # 倒叙用break
                break
                # 顺叙用continue
                #continue
            else:
                # 获取附件
                c_step4_get_email.get_att(msg, str_day)
 
        # print_info(msg)
        server.quit()