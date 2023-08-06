import json
import requests
from requests.exceptions import RequestException
import re
import time
import random
import os
import logging
from lxml import etree
import sys
print(sys.path)
sys.path.append(".")
import time
import jenkins
from openpyxl import load_workbook
from pyocs.pyocs_software import PyocsSoftware
from pyocs import pyocs_software
from pyocs.pyocs_demand import PyocsDemand
from pyocs.pyocs_request import PyocsRequest
from pyocs import pyocs_login
from pyocs.pyocs_list import PyocsList
from pyocs.pyocs_request import PyocsRequest
import logging
from urllib.parse import urlencode
from lxml import etree
from colorama import Fore, Back, Style
from pyocs.pyocs_jenkins import PyocsJenkins
import ltc_interface
import smtplib
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from pyocs import pyocs_email

import platform
#from pyocs import faas_api

import json
import base64


#dirPath = os.getcwd()+'/customers/customer_jinpin/atuo_do_daice_sw'
dirPath = os.getcwd()+'/customers/customer_jinpin/atuo_do_daice_sw'
#window下运行的
#dirPath = os.getcwd()
print("dirPath",dirPath)


def check_if_auto_make_bin(self,str_fangan):
    
    #window下运行时，用这个
    _support_auto_make_bin_file = dirPath+'/support_auto_make_bin.json'
    try:
        logging.info(_support_auto_make_bin_file)
        with open(_support_auto_make_bin_file, 'r') as load_file:
            tmp = load_file.read()
            support_auto_make_bin_dict = json.loads(json.dumps(eval(tmp)))
            if  str(str_fangan) in support_auto_make_bin_dict:
                return support_auto_make_bin_dict[str_fangan]
            else:
                return False                   
            #return support_auto_make_bin_dict
    except FileNotFoundError:
        logging.error("请查找运行路径是否有保存支持自动做bin方案的json文件")
        #先默认支持做bin.支持做bin没什么坏处
        return True

def check_if_project_support_auto_compile(str_fangan):
    
    #window下运行时，用这个
    #getcwd()获取行时所在目录，对运行路径要求苛刻
    _support_auto_make_bin_file = dirPath+'/support_auto_compile.json'
    try:
        logging.info(_support_auto_make_bin_file)
        with open(_support_auto_make_bin_file, 'r') as load_file:
            tmp = load_file.read()
            support_auto_compile_dict = json.loads(json.dumps(eval(tmp)))
            if str(str_fangan) in support_auto_compile_dict:
                return support_auto_compile_dict[str_fangan]
            else:
                return False
            #return support_auto_make_bin_dict
    except FileNotFoundError:
        logging.error("请查找运行路径是否有保存支持自动编译方案的json文件")
        #先默认支持自动编译.支持自动编译稍微浪费了点服务器资源
        return True



def submit_auto_compile(task_id):
    url = "https://tvgateway.gz.cvte.cn/bff-tv-jenkins/api/v1.0/build/build-job"


    user_info = pyocs_login.PyocsLogin.get_account_from_json_file()
    tokens = json.loads(json.dumps(eval(user_info["jenkins_token"])))

    find_customer_material_and_ref_payload = {
        "task_id": task_id,
        "item": [
            "项目组",
        ]
    }





    response = LTC.ltc_get_order_item(find_customer_material_and_ref_payload)
    #print("reuse",response.json())
    if response.status_code==200 and response.json().get("data").get("项目组")!=None:
        print("reuse",response.json())
        project = response.json().get("data").get("项目组")
    else:
        project = ""
    
    check_if_have_submit_auto_flag = False


    #auto_make_bin_flag = do_daice_task.check_if_auto_make_bin(project)
    surport_auto_compile_flag = check_if_project_support_auto_compile(project)
    #check_if_have_submit_auto_flag =self.write_ocs_have_support_auto(task_id)
    #if (check_if_have_submit_auto_flag is True) and (surport_auto_compile_flag is True):
    #surport_auto_compile_flag获取的是string类型
    #if (check_if_have_submit_auto_flag is True) and (str(surport_auto_compile_flag) == "True"):
    if  (str(surport_auto_compile_flag) == "True"):
        print("submit_auto_compile",task_id)
        jenkins_server = jenkins.Jenkins
        if("9632" in project ) or ("9256" in project ) or ("9255" in project ):
            authorization = user_info["Username"] + ":" + tokens["tvci3"]

            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': base64.b64encode(authorization.encode())
            }
            payload = json.dumps({
                    "masterName": "tvci3",
                    "jobUri": "yangpingbu/",
                    "jobName": "Sample_Compile",
                    "params": {
                            "OCS_NUMBER": int(task_id),
                            "AUTO_MAKE_BIN": "False",
                            "COMPILE_SOFTWARE": "True"
                    }
            })
            
        else:
            authorization = user_info["Username"] + ":" + tokens["tvci"]

            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': base64.b64encode(authorization.encode())
            }                        
            payload = json.dumps({
                    "masterName": "tvci",
                    "jobUri": "yangpingbu/",
                    "jobName": "Sample_Compile",
                    "params": {
                            "OCS_NUMBER": int(task_id),
                            "AUTO_MAKE_BIN": "False",
                            "COMPILE_SOFTWARE": "True"
                    }
            })
        ret = requests.request("POST", url, headers=headers, data=payload) 
        print("ret",ret.json()) 

##智能机 1、想找两个相同软件版本且都测试过的 ，一个订单上有多个软件的情况，不能重复积分。
#1 、有emmc bin算3分
#2、emmcbin测试通过1分
# 3、usb和emmc 一样算1分 
# 4 usb测试通过算两分，所以传统机最大是2分

def get_order_score(task_id):
    sw_response = LTC.ltc_get_order_software(task_id)

    score = -1
    sw = sw_response.json().get("data")
    #print("sw",sw)
    score_result = list()
    if sw != None:
        
        for i in range(len(sw)):
            #没软件不算分甚至不参加这个判断，不参加更好
            #result.append(i.get("number"))
            #去掉禁用，有emmc bin且测试通过一般就是最好的条件了
            #还是加一个直接引用对应的软件的功能更好

            score_result.extend([0])
            score = 0
            #score_result[i] = score
            print("score_result",score_result)
            if '禁用' in sw[i].get("active"):
                score = -1
                score_result[i] = score
                continue
            if 'EMMC' in sw[i].get("name"):
                score = 3
            if None != sw[i].get("tested") and '测试通过' == sw[i].get("tested"):
                score = score+1
            score_result[i] = score
            #print(i,score)              
    if not score_result:
        score = max(score_result)
    else:
        score = 0
    return score


def get_max_score_taskid_from_list(task_id_list):
    score_result = list()
    if task_id_list != None:
        
        
        #score_result.append(0)
        check_order_nums = 0
        for task_id in task_id_list:
            sw_response = LTC.ltc_get_order_software(task_id)
            if sw_response.status_code ==200:
                if sw_response.json().get("data") != None:
                    check_order_nums = check_order_nums +1
                    if check_order_nums > 15:
                        break
                    print("task_id in get_max_score_taskid_from_lists",task_id)
                    score_result.append(get_order_score(task_id))
    if score_result:
        i = score_result.index(max(score_result))
    else:
        i = 0         
    
    #print("i",i)
    return task_id_list[i]

class Logger(object):
    def __init__(self, filename='jinpindaice.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger(stream=sys.stdout)
sys.stdout = Logger(stream=sys.stderr)

sys_time=time.strftime('time:%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
print(sys_time)

logging.basicConfig(filename=os.path.join(os.getcwd()+'/customers/customer_jinpin/atuo_do_daice_sw/','log.txt'),level=logging.DEBUG)




LTC = ltc_interface.LtcInterface()

linxiangna_status_need_upload_sw_payload = {
    "searchParams": [{
        "join": "和",
        "maxValue": "",
        "minValue": "",
        "operator": "在",
        "conditionValue": [
            "linxiangna"
        ],
        "condition": "软件工程师",
        "leftParenthesis": "0",
        "rightParenthesis": "0",
        "leftSquareBracket": "0",
        "rightSquareBracket": "0"
    },{
        "join": "和",
        "maxValue": "",
        "minValue": "",
        "operator": "在",
        "conditionValue": [
            "待上传软件"
        ],
        "condition": "当前节点",
        "leftParenthesis": "0",
        "rightParenthesis": "0",
        "leftSquareBracket": "0",
        "rightSquareBracket": "0"
    },{
        "join": "和",
        "maxValue": "",
        "minValue": "",
        "operator": "包含",
        "conditionValue": [
            "生产"
        ],
        "condition": "任务标题",
        "leftParenthesis": "0",
        "rightParenthesis": "0",
        "leftSquareBracket": "0",
        "rightSquareBracket": "0"
    },{
        "join": "和",
        "maxValue": "",
        "minValue": "",
        "operator": "在",
        "conditionValue": [
            "金品"
        ],
        "condition": "下单客户",
        "leftParenthesis": "0",
        "rightParenthesis": "0",
        "leftSquareBracket": "0",
        "rightSquareBracket": "0"
    },{
        "join": "和",
        "maxValue": "",
        "minValue": "",
        "operator": "在",
        "conditionValue": [
            "生产需求"
        ],
        "condition": "分类",
        "leftParenthesis": "0",
        "rightParenthesis": "0",
        "leftSquareBracket": "0",
        "rightSquareBracket": "0"
    },{
        "join": "和",
        "maxValue": "",
        "minValue": "",
        "operator": "在",
        "conditionValue": [
            "TV研发组织"
        ],
        "condition": "申请研发组织",
        "leftParenthesis": "0",
        "rightParenthesis": "0",
        "leftSquareBracket": "0",
        "rightSquareBracket": "0"
    }]
}





status_need_upload_sw_payload = {
    "searchParams": [{
        "join": "和",
        "maxValue": "",
        "minValue": "",
        "operator": "包含",
        "conditionValue": [
            '生产'
        ],
        "condition": "任务标题",
        "leftParenthesis": "0",
        "rightParenthesis": "0",
        "leftSquareBracket": "0",
        "rightSquareBracket": "0"
    },{
        "join": "和",
        "maxValue": "",
        "minValue": "",
        "operator": "在",
        "conditionValue": [
            '金品'
        ],
        "condition": "下单客户",
        "leftParenthesis": "0",
        "rightParenthesis": "0",
        "leftSquareBracket": "0",
        "rightSquareBracket": "0"
    },{
        "join": "和",
        "maxValue": "",
        "minValue": "",
        "operator": "在",
        "conditionValue": [
            '待上传软件'
        ],
        "condition": "当前节点",
        "leftParenthesis": "0",
        "rightParenthesis": "0",
        "leftSquareBracket": "0",
        "rightSquareBracket": "0"
    },{
        "join": "和",
        "maxValue": "",
        "minValue": "",
        "operator": "在",
        "conditionValue": [
            'TV研发组织'
        ],
        "condition": "申请研发组织",
        "leftParenthesis": "0",
        "rightParenthesis": "0",
        "leftSquareBracket": "0",
        "rightSquareBracket": "0"
    },{
        "join": "和",
        "maxValue": "",
        "minValue": "",
        "operator": "包含",
        "conditionValue": [
            '生产需求'
        ],
        "condition": "分类",
        "leftParenthesis": "0",
        "rightParenthesis": "0",
        "leftSquareBracket": "0",
        "rightSquareBracket": "0"
    }]
}

#1、获取待上传软件的订单
#print("status_need_upload_sw_payload",status_need_upload_sw_payload)
"""
order_list = list()
status_need_upload_response = LTC.ltc_search_order_by_advance(status_need_upload_sw_payload)
print("status_need_upload_response.status_code",status_need_upload_response.status_code)
if status_need_upload_response.status_code == 200:
    order_list = status_need_upload_response.json().get("data")
print("order_list",order_list)

if order_list != None:

    for i in range(len(order_list)):
        
        sw_response = LTC.ltc_get_order_software(order_list[i])
        #订单里软件为空。
        if sw_response.json().get("data") == None:
            print("要上传软件的taskid:",order_list[i])



            find_customer_material_and_ref_task_id = order_list[i]
            find_customer_material_and_ref_payload = {
                "task_id": find_customer_material_and_ref_task_id,
                "item": [
                    "客户料号",
                    "软件占空比及电流值"
                ]
            }





            response = LTC.ltc_get_order_item(find_customer_material_and_ref_payload)
            #print("reuse",response.json())

            response_json = response.json()
            customer_material = response_json.get("data").get("客户料号").split("-")[1]
            ref = response_json.get("data").get("软件占空比及电流值")
            #customer_material = 'S67RW27C2000CCC'
            print("customer_material",customer_material)
            #print("ref",ref)
            if customer_material == '':
                continue


            find_reused_payload = {
                "searchParams": [{
                    "join": "和",
                    "maxValue": "",
                    "minValue": "",
                    "operator": "包含",
                    "conditionValue": [customer_material],
                    "condition": "客户料号",
                    "leftParenthesis": "0",
                    "rightParenthesis": "0",
                    "leftSquareBracket": "0",
                    "rightSquareBracket": "0"
                },{
                    "join": "和",
                    "maxValue": "",
                    "minValue": "",
                    "operator": "包含",
                    "conditionValue": [ref],
                    "condition": "软件占空比及电流值",
                    "leftParenthesis": "0",
                    "rightParenthesis": "0",
                    "leftSquareBracket": "0",
                    "rightSquareBracket": "0"
                },{
                    "join": "和",
                    "maxValue": "",
                    "minValue": "",
                    "operator": "在",
                    "conditionValue": [
                        "金品"
                    ],
                    "condition": "下单客户",
                    "leftParenthesis": "0",
                    "rightParenthesis": "0",
                    "leftSquareBracket": "0",
                    "rightSquareBracket": "0"
                },{
                    "join": "和",
                    "maxValue": "",
                    "minValue": "",
                    "operator": "包含",
                    "conditionValue": [
                        "生产"
                    ],
                    "condition": "任务标题",
                    "leftParenthesis": "0",
                    "rightParenthesis": "0",
                    "leftSquareBracket": "0",
                    "rightSquareBracket": "0"
                }]
            }

            #查找相同料号，相同占空比可以引用的库存订单。
            response = LTC.ltc_search_order_by_advance(find_reused_payload)
            #sw = response.json().get("data")
            print("response",response)
            #找到相同的硬件信息的订单不为空。
            if response.status_code == 200:
                if response.json().get("data") != None:
                    #print("response.json()")
                    final_taskid = get_max_score_taskid_from_list(response.json().get("data"))
                    print("final_taskid",final_taskid)
                    reuse_list = list()
                    reuse_list.append(order_list[i])
                    reuse_response = LTC.ltc_copy_software(final_taskid,reuse_list)
                    if reuse_response.status_code == 200 and reuse_response.json().get("message") == 'success':
                        print("引用成功",order_list[i])
                    


##final_taskid= get_max_score_taskid_from_list(['ST22036940'])
##print("final_taskid",final_taskid)
#final_taskid = get_max_score_taskid_from_list(["ST20801613","ST22033787"])
##print("final_taskid",final_taskid)
"""
submit_auto_compile('22045897')