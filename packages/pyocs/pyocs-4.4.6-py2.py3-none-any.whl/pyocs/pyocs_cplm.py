#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import logging
import shutil
import subprocess
import requests
import json
import time
from subprocess import CalledProcessError
from subprocess import Popen, PIPE, STDOUT


class Shell():
    def execute(self, command,useCommunicate=False):
        result = 0
        output = ""
        p = subprocess.Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
        if useCommunicate:
            p.communicate()
            result = p.returncode
        else:
            p.wait()
            result = p.returncode
            output = p.stdout.read().decode("utf-8")
        return result,output

class PyocsCplm:
    _logger = logging.getLogger(__name__)
    _var_www_sw_bin = '/var/www/sw_bin/'

    def __init__(self):
        self._logger.setLevel(level=logging.INFO)  # 控制打印级别
        self.shell = Shell()
        self.cplmBffUrl = "https://tvgateway.gz.cvte.cn/bff-cplm-front"
        self.sw_www_path = None
        self.xml_www_path = None
        self.task_id = None


    def clean_var_www_sw_bin_files(self):
        if self.sw_www_path and os.path.exists(self.sw_www_path):
            os.remove(self.sw_www_path)
        if self.xml_www_path and os.path.exists(self.xml_www_path):
            os.remove(self.xml_www_path)


    def convert_ocs_to_cplm_num(self, ocs_id):
        task_id = None
        search_url = "https://faas.gz.cvte.cn/function/cplm-transform-ocs-num"
        payload = {
            "ocs_num":ocs_id,
            "env":"prod"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", search_url, headers=headers, json=payload)
        ret_json = json.loads(response.text)

        if ret_json["data"]:
            task_id = ret_json["data"]["cplm_task_id"]
        return task_id


    def get_xml_attr(self, xml_path, attr_name):
        attr_val = ''
        pattern_name = re.compile(r'Name=".*?"')
        pattern_value = re.compile(r'Atoms=".*?"')
        with open(xml_path, 'r') as f:
            for line in f.readlines():
                if attr_name in line:
                    tmp_name = pattern_name.search(line).group()
                    tmp_name = tmp_name.replace("Name=", "").replace('"', '')
                    if attr_name == tmp_name:
                        attr_val = pattern_value.search(line).group()
                        attr_val = attr_val.replace("Atoms=", "").replace('"', '')
        return attr_val


    def get_task_id(self, xml_path):
        task_id = self.get_xml_attr(xml_path, "SW_OCSID")
        if len(task_id) <= 6:
            return self.convert_ocs_to_cplm_num(task_id)
        else:
            return ("ST" + task_id)


    def get_product_model(self, xml_path):
        subCode = self.get_xml_attr(xml_path, "SW_Chipset_SubCode")
        product_model = self.get_xml_attr(xml_path, "SW_Chipset")
        if "/" in product_model:
            product_model = product_model.split("/")[0]
        if subCode:
            product_model = product_model.replace(subCode,"")
        if "_" in product_model:
            product_model = product_model.split("_")[0]
        if product_model[-1] >= "A" and product_model[-1] <= "G":
            product_model = list(product_model)
            product_model.pop()
            product_model = "".join(product_model)
        return product_model


    def copy_software_to_var_www_sw_bin(self, software):
        """
        将软件拷贝到http服务器的默认路径下，并返回对应文件的路径
        """
        xml_path = None
        xml_www_path = None
        sw_www_path = None

        if software is None:
            self._logger.error("软件包路径不正确！")
            return sw_www_path, xml_www_path
        elif os.path.exists(software):
            # 参数是USB软件包的情况
            xml_path = software.split('.')[0] + '.xml'
            # 参数是EMMC BIN的情况
            if not os.path.exists(xml_path):
                if '/' in software:
                    for filename in os.listdir(os.path.dirname(software)):
                        if ".xml" in filename:
                            try:
                                pattern_sw_buildtime = re.compile(r'\d{4}[0-1]\d[0-3]\d_[0-2]\d([0-5]\d){2}')
                                sw_buildtime = pattern_sw_buildtime.search(filename).group()
                                if sw_buildtime in software:
                                    xml_path = os.path.dirname(software) + '/' + filename
                            except AttributeError:
                                self._logger.debug("xml文件:%s" % filename + "与软件包不匹配!")
                else:
                    for filename in os.listdir('./'):
                        if ".xml" in filename:
                            try:
                                pattern_sw_buildtime = re.compile(r'\d{4}[0-1]\d[0-3]\d_[0-2]\d([0-5]\d){2}')
                                sw_buildtime = pattern_sw_buildtime.search(filename).group()
                                if sw_buildtime in software:
                                    xml_path = filename
                            except AttributeError:
                                self._logger.debug("xml文件:%s" % filename + "与软件包不匹配!")


        if xml_path is None:
            self._logger.error("软件包或软件的XML路径不正确！")
            return sw_www_path, xml_www_path
        elif os.path.exists(xml_path) and os.path.exists(software):
            xml_www_path = shutil.copy2(xml_path, self._var_www_sw_bin)
            sw_www_path = shutil.copy2(software, self._var_www_sw_bin)
            os.chmod(xml_www_path, 0o666)
            os.chmod(sw_www_path, 0o666)
            return sw_www_path, xml_www_path
        else:
            self._logger.error("软件包或软件的XML路径不正确！")
            return sw_www_path, xml_www_path


    def get_software_and_xml_url(self, sw_www_path, xml_www_path):
        usb_sw_url = None
        xml_url = None
        emmc_bin_url = None
        # 解析本机IP
        if not os.getenv('LOCAL_IP'):
            result,output = self.shell.execute("cat /etc/network/interfaces | grep '^\s*address' | awk -F' ' '{print $2}'")
            ip = output.replace("\n","")
        else:
            ip = os.getenv('LOCAL_IP')

        if xml_www_path:
            xml_url =xml_www_path.replace(self._var_www_sw_bin, 'http://' + ip +'/sw_bin/')
        if sw_www_path:
            sw_url = sw_www_path.replace(self._var_www_sw_bin, 'http://' + ip +'/sw_bin/')
        return sw_url, xml_url


    def get_burning_info(self, task_id, product_model, software):
        # 获取数据
        url = self.cplmBffUrl + "/api/v1.0/sw-task-info/get-pcb-designators-by-task-num?taskNum={}&productModel={}".format(task_id, product_model)
        response = requests.request("GET", url)
        retJson = json.loads(response.text)
        taskNum = None
        if not retJson["data"] or len(retJson["data"]) <= 0:
            # 改用订单查询产品型号
            url = self.cplmBffUrl + "/api/v1.0/sw-task-info/get-sw-task-product-model?taskNum={}".format(task_id)
            response = requests.request("GET", url)
            retJson = json.loads(response.text)
            if not retJson["data"]:
                self._logger.error("获取订单产品型号失败!")
                return 1
            else:
                self.productModel = retJson["data"]
            url = self.cplmBffUrl + "/api/v1.0/sw-task-info/get-pcb-designators-by-task-num?taskNum={}&productModel={}".format(task_id, product_model)
            response = requests.request("GET", url)
            retJson = json.loads(response.text)
        if not retJson["data"] or len(retJson["data"]) <= 0:
            return 1
        # 数据解析
        if (product_model == "TPD.NT72691.PC821") or (product_model == "TD.NT72691.81"):
            software_name = software.upper()
            pcb_designator = " "
            burning_method = "离线烧录"

            if software_name.startswith("NORFLASH"):
                for flashData in retJson["data"]:
                    if flashData["minClass"] == "NOR FLASH":
                        pcb_designator = flashData["designator"]
                        break
            elif software_name.startswith("EEPROM"):
                for flashData in retJson["data"]:
                    if flashData["minClass"] == "EEPROM":
                        pcb_designator = flashData["designator"]
                        break
            elif software_name.startswith("EMMCBIN"):
                for flashData in retJson["data"]:
                    if flashData["minClass"] == "EMMC FLASH":
                        pcb_designator = flashData["designator"]
                        break
            else: #其余都当作USB软件包
                for flashData in retJson["data"]:
                    if flashData["minClass"] == "EMMC FLASH":
                        pcb_designator = flashData["designator"]
                        burning_method = "在线烧录"
                        break
            return pcb_designator, burning_method


        else: # 当前自研主流TV公版平台方案只有一个FLASH，烧录位号、烧录方式获取方式
            flashData = {}
            for oneFlash in retJson["data"]:
                minClass = oneFlash["minClass"]
                if minClass == "EMMC FLASH" or minClass == "NAND FLASH" or minClass == "EEPROM" or minClass == "NOR FLASH":
                    flashData = oneFlash
                    break
            pcb_designator = flashData["designator"]
            if flashData["minClass"] == "EMMC FLASH" or flashData["minClass"] == "NAND FLASH":
                if "EMMCBIN" in software:
                    burning_method = "离线烧录"
                else:
                    burning_method = "在线烧录"
            elif flashData["minClass"] == "NOR FLASH":
                burning_method = "离线烧录"
            return pcb_designator, burning_method


    def get_test_type_by_cmd_param(self, test_type):
        if test_type == "N":
            is_need_test = "否"
            return is_need_test, test_type
        else:
            is_need_test = "是"
            if test_type == "A":
                test_type = "A类 - 全面测试"
            elif test_type == "B+C":
                test_type = "B+C - 新遥控器测试，局部功能修改/添加"
            elif test_type == "B":
                test_type = "B类 - 针对遥控器的测试"
            elif test_type == "C":
                test_type = "C类 - 局部修改针对性测试"
            elif test_type == "D":
                test_type = "D类 - 测配屏"
            elif test_type == "E":
                test_type = "E类 - 首测，无任何功能及BUG的修改"
            elif test_type == "F":
                test_type = "F类 - 过硬件首测，只要求匹配硬件"
            elif test_type == "G":
                test_type = "G类 - 仅测试BOOT"
            else:
                self._logger.error("测试类型输入有误！")
        return is_need_test, test_type


    def check_upload_param(self, upload_body):
        if isinstance(upload_body, dict):
            for key,value in upload_body.items():
                if value is None:
                    self._logger.info("上传参数有误！")
                    return False
            return True


    def get_cplm_upload_software_parma(self, task_id, software, test_type):
        if not os.getenv('UPLOAD_OCS_USER'):
            user = os.getenv('USER')
        else:
            user = os.getenv('UPLOAD_OCS_USER')
        self._logger.info("软件上传人: "+ user)

        self.sw_www_path, self.xml_www_path = self.copy_software_to_var_www_sw_bin(software)
        if self.sw_www_path and self.xml_www_path:
            sw_url, xml_url = self.get_software_and_xml_url(self.sw_www_path, self.xml_www_path)
        else:
            return

        sw_name = None
        xml_name = None
        if sw_url:
            sw_name = sw_url.split('/')[-1]
        if xml_url:
            xml_name = xml_url.split('/')[-1]

        if task_id is None:
            task_id = self.get_task_id(self.xml_www_path)
        self._logger.info("软件任务: "+ str(task_id))

        product_model = self.get_product_model(self.xml_www_path)
        self._logger.info("产品型号: "+ product_model)

        pcb_designator, burning_method = self.get_burning_info(task_id, product_model, software)
        self._logger.info("烧录位号: "+ pcb_designator)
        self._logger.info("烧录方式: "+ burning_method)

        is_need_test, test_type = self.get_test_type_by_cmd_param(test_type)
        self._logger.info("是否测试: "+ is_need_test)
        self._logger.info("测试类型: "+ test_type)

        upload_body = {
                "userAccount":user,
                "softwareTaskId":task_id,
                "fwUrl":sw_url,
                "fwFileName":sw_name,
                "xmlUrl":xml_url,
                "xmlFileName":xml_name,
                "productModel":product_model,
                "isNeedTest":is_need_test,
                "testType":test_type,
                "pcbDesignator":pcb_designator,
                "burningMethod":burning_method,
                "swPurpose":"生产软件",
            }

        return upload_body


    def upload_software_to_cplm_soft_task_api(self, upload_body):
        ret_status = False
        if self.check_upload_param(upload_body):
            self._logger.info("开始上传...")
            try_upload_cnt = 0
            while True:
                upload_url = self.cplmBffUrl + "/api/v1.0/fw-upload/upload-firmware"
                headers = {
                        'Content-Type': 'application/json',
                    }
                payload = json.dumps(upload_body)
                if try_upload_cnt > 0:
                    upload_body["isView"] = True
                response = requests.request("POST", upload_url, headers=headers, data=payload)
                ret_json = json.loads(response.text)
                if  ret_json["data"]["resultStatus"] == "成功" or ( ret_json["data"]["resultMsg"] and "不能添加重复固件" in ret_json["data"]["resultMsg"]):
                    ret_status = True
                    self._logger.info("上传成功!")
                    try:
                        itemId = ret_json["data"]["itemId"]
                        if itemId:
                            search_url = self.cplmBffUrl + "/api/v1.0/fw-download/get-task-sw-xml-url-by-id"
                            payload = json.dumps({
                                "firmwareDetailId":itemId
                            })
                            headers = {
                                'Content-Type': 'application/json',
                            }
                            response = requests.request("POST", search_url, headers=headers, data=payload)
                            url_ret = json.loads(response.text)
                            if url_ret["status"] == "0":
                                self._logger.info("软件链接 "+ url_ret["data"]["swUrl"])
                                self._logger.info("xml链接 "+ url_ret["data"]["xmlUrl"])
                    except:
                        self._logger.info("获取链接失败!")
                    break
                if try_upload_cnt >= 12:
                    self._logger.warn("上传失败!")
                    self._logger.info("-------- upload_body --------")
                    self._logger.info(upload_body)
                    self._logger.info("-------- ret_json --------")
                    self._logger.info(ret_json)
                    break
                time.sleep(30)
                try_upload_cnt += 1
        return ret_status
