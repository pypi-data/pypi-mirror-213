#! /usr/bin/python3
# -*- coding: utf-8 -*-
import os
import wget
from Mail import Mail
from ApkSign import *
from Constant import BASE_PATH
import re
#1、获取邮件
#2、识别战术邮件。下载附件
#3、签名，获取附件（我增加一个功能，获取签名类型。以及 使用帮助）
#4、发送邮件
#5、清理工作

def parse_string_from_info(subjest_info,string_pattern):
    pattern = re.compile(string_pattern, re.S)
    #print(pattern)
    items = re.findall(pattern, subjest_info)
    return items


if __name__ == '__main__':
    
    m = Mail('account','passwd')
    mailID = m.getSpecialSubjectMail('【APK自动签名】')
    if mailID == -1:
        print("没有需要处理的\n")
        
    attachmentList = m.getApkFromMail(mailID)
    print(attachmentList)
    mailFromAddr = m.getMailFromAddr(mailID)
    print(mailFromAddr)


    Mailsubject = m.getMailsubject(mailID)
    print("Mailsubject",Mailsubject)

    if '【使用帮助】' in Mailsubject:
        m.sendMailhelptext(mailFromAddr)
        exit(0)

    string_pattern='signType-(.*?)】'
    signType = parse_string_from_info(Mailsubject,string_pattern)
    signType =str(signType)
    signType = signType[2:-2]
    print("signType",signType)
    signtype_list = get_signApk_type()
    if signType in signtype_list:
        print("TRUE")
    #signType = 'aml962x2'
    signedAPKList = list()
    for file in attachmentList:
        signedAPKDownloadUrl = signApk(signType,file)
        downLoadFileName = wget.download(signedAPKDownloadUrl, out=file.replace('.apk','') + '-' + signType +'-signed.apk')
        print('\n')
        signedAPKList.append(os.path.join(BASE_PATH, downLoadFileName))

    m.sendMailWithAttachment(mailFromAddr,signedAPKList)

    #step3 清尾，删除中间文件
    for i in attachmentList:
        os.remove(i)
    for i in signedAPKList:
        os.remove(i)
