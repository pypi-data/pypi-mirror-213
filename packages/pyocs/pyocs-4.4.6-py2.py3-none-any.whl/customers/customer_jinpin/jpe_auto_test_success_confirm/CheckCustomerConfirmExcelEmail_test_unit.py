import datetime
import email
import poplib
poplib._MAXLINE=204800#重设行长度
import email.policy
import telnetlib
import time
import os
import json
import re
import sys
from openpyxl import load_workbook
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from pyocs import pyocs_login
import global_var as gl    #添加全局变量管理模块
pop3_server = 'pop.cvte.com'
poplib._MAXLINE=20480
#=============================================================
# 脚本介绍和说明：
# 1、在CVTE企业网页邮箱里设置把收取3个月的邮件改成收取全部
# 2、这个脚本第一次运行会生产一个文件counttxt.txt记录目前邮件数
# 3、下次运行会获取最新的邮件的数，然后处理新增的邮件
#==============================================================
gl._init()
class CheckCustomerConfirmExcelEmail:



    def get_vidaa_version(self, text):

        #regular = re.compile(r'）(*.?)<')
        #tmp = re.findall(regular, text)
        tmp = text.split('<br')[0].rsplit('）')[0].rsplit(')')[0]
        print("get_just_sw_number tmp =",tmp)
        if tmp:
            return tmp[0]
        else:
            return text            



#==============================================================
# 主程序
# 登录邮箱。获取邮件个数，对比处理新增邮件个数
# 将名称含有subject_title 特殊字符的邮件才进行解析处理。
#==============================================================
if __name__ == '__main__':
        # 连接到POP3服务器,有些邮箱服务器需要ssl加密，可以使用poplib.POP3_SSL
    #text = 'CP796208_JPE_VT0143FB1_0103_MT9602_PB801_KENYA_SG4251B03_3_IR_R45MMI804_Logovnp_PID8_7KEY_r20221017_170725_C_2K_AU_V0103.01.00O.M0916.zip<br/>二次(配置)包软件：针对订单-T-CON板软件-PT430CT02-5-DCBHM-H260A_01-VESA'
    text = 'CP796208_JPE_VT0143FB1_0103_MT9602_PB801_KENYA_SG4251B03_3_IR_R45MMI804_Logovnp_PID8_7KEY_r20221017_170725_C_2K_AU_V0103.01.00O.M0916.zip'

    text_email_acquire = CheckCustomerConfirmExcelEmail()
    text_email_acquire.get_vidaa_version(text)