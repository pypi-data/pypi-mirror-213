import re
from lxml import etree
import logging
from pyocs.pyocs_request import PyocsRequest
from pyocs.pyocs_exception import *
import requests
import bs4
import json
import re


class PyocsDemand:
    _ocs_link_Prefix = 'https://ocs-api.gz.cvte.cn/tv/Tasks/view/'
    _logger = logging.getLogger(__name__)





    product_name = "产品型号"
    requirement_nums = "需求数量"
    chip_name = "主芯片"
    flash_size_name = "FlashSize"
    flash_info = "Flash信息"
    port_name = "子板型"
    port_info = "板卡端子信息"
    ddr_name = "ddrSize"
    region_name = "区域"
    ciplus_name = "CI PLUS功能"
    pwm_name = "占空比"
    tuner_name = "高频头"
    title_name = "Title"
    task_type = "任务类型"
    task_stage = "任务阶段"
    customer_batch_code = "客户批号"
    customer_machine = "客户机型"
    other_app_soft = "其它应用软件"
    wifi_bluetooth_type = "WIFI与蓝牙"
    wifi_bluetooth_info = "WIFI与蓝牙信息"
    ci_type = "可选功能CI类型"
    wifi_module_info = "可选功能WIFI模块"
    chip_remark = "主芯片备注"
    customer_special_requirement = "客户特殊需求"
    option_func = "可选功能"
    tv_system = "电视制式"
    ddr_info = "存储器信息"
    task_comment_area = "评论区"
    produce_batch_code = "生产批号"
    software_tracker = "软件跟踪人员"
    opm = "高级经理"
    nq = "负责内勤"
    ebs_num = "EBS订单编号"
    sw_branch_path = "分支量产状态"
    os_system = "OS系统"

    SAMPLE_ORDER = "样品订单"
    FORMAL_ORDER = "正式订单"

    # 样品订单获取方案名依赖的是产品型号，因为会依据方案名维护配置仓库，防止出现多个相同的仓库，为与正式订单维持一致，需要做一层映射
    project_map_dict = {
        "MS358": "MSD358",
        "RD8503": "RDA8503",
        "SK706": "MT9632",
        "SK708D": "T972",
        "SK508": "HV35X",
        "SK702": "HV56X",
        "ATM30": "T920L",
        "MT9256": "SK516",
        "SK513": "T950D4",
        "SK105A": "UTS6710"
    }


    def __init__(self, ocs_number=""):
        self.ocs_number = ocs_number

        if "ST" in self.ocs_number:
            self.ocs_number = self.ocs_number.replace("ST", "")

        self._logger.setLevel(level=logging.WARNING)  # 控制打印级别
        url = "https://faas.gz.cvte.cn/function/cplm-get-order-item"

        item_payload_type = {
            "task_id": self.ocs_number,
            "item": [
                "分类"
            ]
        }

        item_payload_product = {
            "task_id": self.ocs_number,
            "item": [
                "产品型号",
                "项目组",
                "分类",
                "产品代码",
                "下单客户",
                "主芯片",
                "FlashSize",
                "端子功能",
                "高频头",
                "CI PLUS功能",
                "软件占空比及电流值",
                "客户批号",
                "客户机型",
                "其它应用软件",
                "可选功能",
                "WIFI与蓝牙",
                "External DDR",
                "客户特殊需求",
                "互联网电视牌照",
                "浏览器",
                "OS系统",
                "应用商店",
                "默认国家/地区",
                "生产批次",
                "散件类型",
                "需求数量",
                "电视制式"
            ]
        }

        item_payload_sample = {
            "task_id": self.ocs_number,
            "item": [
                "产品型号",
                "项目组",
                "分类",
                "产品代码",
                "下单客户",
                "主芯片",
                "FlashSize",
                "端子功能",
                "高频头",
                "CI PLUS功能",
                "软件占空比及电流值",
                "软件占空比",
                "客户批号",
                "客户机型",
                "其它应用软件",
                "可选功能",
                "WIFI与蓝牙",
                "External DDR",
                "客户特殊需求",
                "互联网电视牌照",
                "浏览器",
                "OS系统",
                "应用商店",
                "默认国家/地区",
                "电视制式"
            ]
        }

        headers = {
            'Content-Type': 'application/json'
        }


        response = requests.request("POST", url, headers=headers, json=item_payload_type)

        if response.status_code == 200:
            self._logger.info(response.json())
            self.Ltcresponsejson = response.json()
            self._logger.info(self.Ltcresponsejson)
            if "发样任务" in self.Ltcresponsejson.get("data").get("分类"):
                response = requests.request("POST", url, headers=headers, json=item_payload_sample)
                self.order_type = self.SAMPLE_ORDER
            else:
                response = requests.request("POST", url, headers=headers, json=item_payload_product)
                self.order_type = self.FORMAL_ORDER

            self.Ltcresponsejson = response.json()
            self._logger.info(self.Ltcresponsejson)

            url = "https://faas.gz.cvte.cn/function/cplm-get-pcm-detail-info"


            headers = {
                'Content-Type': 'application/json'
            }
            detail_item_payload = {
                "hw_code": self.Ltcresponsejson.get("data").get("产品代码"),
                "item": [
                    "客户特殊需求",
                    "External DDR"
                    ]
            }

            self.Ltcdetail_response = requests.request("POST", url, headers=headers, json=detail_item_payload)
            if self.Ltcdetail_response.status_code == 200:
                self._logger.info(self.Ltcdetail_response.json())

        else:
            raise OcsSystemError('LTC访问存在问题')



    def get_passenger_number(self):
        passengernum_list = list()
        passengernum_list.append(self.Ltcresponsejson.get("data").get("客料号"))         
        passengernum_str = "".join(passengernum_list).strip('\n').strip() if passengernum_list else ""
        passengernum_str = passengernum_str.split("，")
        for i in passengernum_str:
            if "客料号" in i:
                return i.split("）")[0].split("客料号")[-1]

    def get_summary(self):
        summary_xpath = '//title'
        summary_list = self.html.xpath(summary_xpath)
        summary_str = "".join(summary_list[0].text).strip() if summary_list else ""
        return summary_str

    def get_flash_model(self):
        flash_model_xpath = '//*[@id="orderinfo_hw"]//th[contains(text(),"FlashSize")]/../td/p[contains(text(),"FLASH")]/text()'
        flash_model_list = self.html.xpath(flash_model_xpath)
        flash_model_str = "".join(
        flash_model_list).strip() if flash_model_list else ""  # 删除开头与结尾的空白符（包括'\n', '\r',  '\t',  '')
        return flash_model_str
        # flash_model_list = ("".join(flash_model_str).split("FLASH型号："))  # [-1]

    def get_chipset_name(self):
        # 板卡型号
        chipset_xpath = '//*[@id="req_region"]/div[2]/div[1]/div/p[1]/strong[1]/a/text()'
        chipset_list = self.html.xpath(chipset_xpath)
        chipset_str = "".join(chipset_list).strip('\n').strip() if chipset_list else ""
        chipset_str = chipset_str.split("<")[0]
        return chipset_str

    def get_flag_color(self):
        flag_color_xpath = '//span/i/@*'
        flag_color_list = self.html.xpath(flag_color_xpath)
        for each in flag_color_list:
            if 'icon-flag-' in each:
                return each[10:]    # 第11个字符以后的字符串


    def get_ocs_html(self):
        return self.html

    def get_ocs_number(self):
        return self.ocs_number

    def get_ocs_software_engineer(self):
        if self.order_type == self.FORMAL_ORDER:
            t_xpath = '//*[@id="basicinfo_region"]//*[@id="Task__sw_user_id_history"]/../span/text()'
            t_list = self.html.xpath(t_xpath)
            t_str = "".join(t_list[0]).strip() if t_list else ""  # 删除开头与结尾的空白符（包括'\n', '\r',  '\t',  ' ')
            self._logger.info("软件工程师：" + str(t_str))
            return t_str
        else:
            return ""

    def get_ocs_ckd_info(self):
        if self.order_type == self.FORMAL_ORDER:
            t_str = self.Ltcresponsejson.get("data").get("散件类型")
            self._logger.info("CKD Info" + str(t_str))
            return t_str
        else:
            return ""

    def get_ocs_customer(self):
        if self.order_type == self.FORMAL_ORDER:
            t_str = self.Ltcresponsejson.get("data").get("下单客户")
            self._logger.info("客户：" + str(t_str))
            return t_str
        elif self.order_type == self.SAMPLE_ORDER:
            return "CVTE样品"
        else:
            return ""

    def get_ocs_stock_real_customer(self):
        if self.order_type == self.FORMAL_ORDER:
            t_str = self.Ltcresponsejson.get("data").get("备货主客户")
            self._logger.info("备货主客户" + str(t_str))
            return t_str
        elif self.order_type == self.SAMPLE_ORDER:
            return "CVTE样品"
        else:
            return ""

    def get_ocs_title(self):
        t_xpath = '//title/text()'
        t_list = self.html.xpath(t_xpath)
        t_str = "".join(t_list).strip() if t_list else ""  # 删除开头与结尾的空白符（包括'\n', '\r',  '\t',  ' ')
        self._logger.info("Title：" + str(t_str))
        return t_str

    def get_ocs_project_name(self): 
        if self.Ltcresponsejson.get("data").get("项目组") !=None:
            project_name = self.Ltcresponsejson.get("data").get("项目组")
            return project_name
        else:
            return ""

    def get_product_name(self):
        product_str = self.Ltcresponsejson.get("data").get("产品型号")
        self._logger.info("产品型号：" + str(product_str))
        return product_str

    def get_requirement_nums(self):
        require_xpath = \
            '//th[contains(text(),"需求数量")]/../td/text()'
        require_list = self.html.xpath(require_xpath)
        require_str = "".join(require_list).strip().strip('\r\n') if require_list else ""
        self._logger.info("需求数量：" + str(require_str))
        return require_str

    def get_region_name(self):

        region_list = list()
        region_list.append(self.Ltcresponsejson.get("data").get("默认国家/地区"))            
        region_str = "".join(region_list).strip() if region_list else ""
        region_str = "" if region_str == '无' else region_str
        self._logger.info("区域：" + str(region_str))
        return region_str


    def get_ci_plus(self):
        if self.Ltcresponsejson.get("data").get("CI PLUS功能"):
            ciplus_list = list()
            ciplus_list.append(self.Ltcresponsejson.get("data").get("CI PLUS功能"))
            ciplus_str = "".join(ciplus_list).strip() if ciplus_list else ""
            ciplus_str = "" if ciplus_str == '无' else ciplus_str
            self._logger.info("CI+：" + str(ciplus_str))
            return ciplus_str
        else:
            return ""

    def get_pwm(self):
        pwm_str = self.Ltcresponsejson.get("data").get("软件占空比及电流值")
        if self.order_type == self.SAMPLE_ORDER:
            pwm_str = pwm_str if pwm_str else self.Ltcresponsejson.get("data").get("软件占空比")

        if pwm_str:
            pwm_str = "".join(pwm_str).strip()
            self._logger.info("占空比：" + str(pwm_str))
            if pwm_str == '无':
                pwm = '100'
            else:
                pwm_pattern = re.compile('(100|[0-9]{1,2})%')
                pwm_str_list = pwm_pattern.findall(pwm_str)
                if not pwm_str_list:
                    raise ReadPwmError('占空比读取错误')
                pwm = pwm_str_list[0].strip('%')
                # pwm_original = pwm_str.split('=')
                # pwm = pwm_original[1].strip(')').strip('%')
        else:
            pwm = '100'
        return pwm


    def get_customer_machine(self):
        if self.order_type == self.FORMAL_ORDER:
            if self.Ltcresponsejson.get("data").get("客户机型") != None:
                product_list = list()
                product_list.append(self.Ltcresponsejson.get("data").get("客户机型"))
                product_str = "".join(product_list).strip().strip('\r\n') if product_list else ""
                product_str = product_str if product_str else ""
                if product_str:
                    pattern = re.compile(r'\w*\w')
                    product_str = pattern.search(product_str).group()
                self._logger.info("客户机型：" + str(product_str))
            else:
                product_str = ''
            return product_str
        elif self.order_type == self.SAMPLE_ORDER:
            return ""
        else:
            return ""

    def get_other_app_software(self):
        if self.order_type == self.FORMAL_ORDER:
            app_list = list()
            app_list.append(self.Ltcresponsejson.get("data").get("其它应用软件"))               
            app_str = "".join(app_list).strip() if app_list else ""
            app_str = "" if app_str == '无' else app_str
            self._logger.info("其它应用软件：" + str(app_str))
            return app_str
        elif self.order_type == self.SAMPLE_ORDER:
            app_list = list()
            app_list.append(self.Ltcresponsejson.get("data").get("互联网电视牌照"))                
            app_str = "".join(app_list[0]).strip() if app_list else ""
            app_str = "" if app_str == '无' else app_str
            return app_str
        else:
            return ""

    def get_chip_name(self):
        chip_list = list()
        chip_list.append(self.Ltcresponsejson.get("data").get("主芯片"))        
        chip_str = "".join(chip_list).strip('\n').strip() if chip_list else ""
        self._logger.info("主芯片：" + chip_str)
        return chip_str

    def get_panel_info(self):
        xpath_ret_list = list()
        xpath_ret_list.append(self.Ltcresponsejson.get("data").get("驱屏接口"))          
        ret = "".join(xpath_ret_list).strip('\n').strip() if xpath_ret_list else ""
        self._logger.info("驱屏接口：" + ret)
        return ret

    def get_pmic_type(self):
        xpath_ret_list = list()
        xpath_ret_list.append(self.Ltcresponsejson.get("data").get("PMIC型号"))             
        ret = "".join(xpath_ret_list).strip('\n').strip() if xpath_ret_list else ""
        self._logger.info("PMIC型号" + ret)
        return ret

    def get_gamma_type(self):
        xpath_ret_list = list()
        xpath_ret_list.append(self.Ltcresponsejson.get("data").get("GAMMA型号"))         
        ret = "".join(xpath_ret_list).strip('\n').strip() if xpath_ret_list else ""
        self._logger.info("GAMMA型号" + ret)
        return ret

    def get_chip_remark(self):
        chip_remark_str = ''
        """
        #暂时用不上了
        if self.Ltcresponsejson.get("data").get("主芯片") != None:
            chip_remark_list = list()
            chip_remark_list.append(self.Ltcresponsejson.get("data").get("主芯片"))    
            chip_remark_str = "".join(chip_remark_list).strip('\n').strip() if chip_remark_list else ""
            self._logger.info("主芯片备注：" + chip_remark_str)
        """

        return chip_remark_str

    def get_flash_info(self):
        flash_size_list = list()
        flash_size_list.append(self.Ltcresponsejson.get("data").get("FlashSize"))          
        flash_str = "".join(flash_size_list) if flash_size_list else ""
        self._logger.info("Flash信息：" + flash_str)
        return flash_str

    def get_flash_size(self):
        flash_size_list = list()
        flash_size_list.append(self.Ltcresponsejson.get("data").get("FlashSize"))   
        if flash_size_list:
            flash_str_original = flash_size_list[0].split('使用')
            flash_digital_list = re.findall(r"(.+?)Byte", flash_str_original[-1])
            if flash_digital_list:
                flash_size = flash_digital_list[0]
                self._logger.info("flash size：" + flash_size)
                return flash_size
            else:
                return ""
        else:
            return ""

    def get_port_name(self):
        port_list = list()
        port_list.append(self.Ltcresponsejson.get("data").get("端子功能"))           
        port_str_orinal = "".join(port_list).strip() if port_list else ""
        if port_str_orinal:
            port_str = port_str_orinal.strip().split(']')[0].split('[')[1]
            self._logger.info("子板型：" + str(port_str))
            return port_str
        else:
            return ""

    def get_port_info(self):
        port_list = list()
        port_list.append(self.Ltcresponsejson.get("data").get("端子功能"))         
        port_str_orinal = "".join(port_list).strip() if port_list else ""
        if port_str_orinal:
            self._logger.info("板卡端子信息：" + str(port_str_orinal))
            return port_str_orinal
        else:
            return ""

    def get_ddr_size(self):
        """
        summary
            External DDR 的描述有两种情况，如下
            1. External DDR: 使用三星DDR】使用1GByte（8Gbit）的DDR芯片
            2. External DDR: 2133Mbps 512MB+1866Mbps 256MB混搭】使用768MByte（6Gbit） 的DDR芯片
        Returns:
            [type] -- [description]
        """
        if self.Ltcresponsejson.get("data").get("External DDR") and self.Ltcresponsejson.get("data").get("主芯片"):
            ddr_list_0 = list()
            ddr_list_0.append(self.Ltcresponsejson.get("data").get("主芯片"))         
            ddr_list_1 = list()
            ddr_list_1.append(self.Ltcresponsejson.get("data").get("External DDR"))
            if self.Ltcdetail_response.status_code == 200 and self.Ltcdetail_response.json().get("data")!= None: 
                External_DDR_remark = ''
                ddr_list_2 = list()
                for detail_data in self.Ltcdetail_response.json().get("data"):
                    for x,y in detail_data.items():
                        if x == 'External DDR':
                            External_DDR_remark = detail_data.get("特殊备注")
                            break
                self._logger.info("get ddr",External_DDR_remark)
                ddr_list_2.append(External_DDR_remark)                
            chip_desc_str = "".join(ddr_list_0) if ddr_list_0 else ''
            ddr_str_1 = "".join(ddr_list_1) if ddr_list_1 else ''
            ddr_str_2 = "".join(ddr_list_2) if ddr_list_2 else ''
            external_ddr_str = ddr_str_1 + ddr_str_2

            self._logger.info("chip_desc_str",chip_desc_str)
            self._logger.info("external_ddr_str",external_ddr_str)

            if external_ddr_str:
                if "总内存是" in external_ddr_str:
                    ddr_original_str = external_ddr_str.split('总内存是')
                    ddr_digital_list = re.findall(r"(.+?)B", external_ddr_str[-1])
                    if ddr_digital_list:
                        ddr_size = ddr_digital_list[0]
                        self._logger.info("ddr size：" + ddr_size)
                        return ddr_size
                    else:
                        return ""
                elif "共内存是" in external_ddr_str:
                    ddr_original_str = external_ddr_str.split('共内存是')
                    ddr_digital_list = re.findall(r"(.+?)B", ddr_original_str[-1])
                    if ddr_digital_list:
                        ddr_size = ddr_digital_list[0]
                        self._logger.info("ddr size：" + ddr_size)
                        return ddr_size
                    else:
                        return ""
                else:
                    ddr_original_str = external_ddr_str.split('使用')
                    ddr_digital_list = re.findall(r"(.+?)Byte", ddr_original_str[-1])
                    if ddr_digital_list:
                        ddr_size = ddr_digital_list[0]
                        self._logger.info("ddr size：" + ddr_size)
                        return ddr_size
                    else:
                        return ""
            else: # 如果 externel ddr 不存在，就去主芯片描述去找
                if "内置" in chip_desc_str:
                    ddr_original_str = chip_desc_str.split('内置')
                    ddr_digital_list = re.findall(r"(.+?)B", ddr_original_str[-1])
                    if ddr_digital_list:
                        ddr_size = ddr_digital_list[0]
                        self._logger.info("ddr size：" + ddr_size)
                        return ddr_size
                    else:
                        return ""
                else:
                    return ""
            self._logger.info("DDR：" + str(ddr_size))
        else:
            ddr_size =''
        return ddr_size

    def get_tuner_type(self):
        if self.Ltcresponsejson.get("data").get("高频头") != None:
            tuner_list = list()
            tuner_list.append(self.Ltcresponsejson.get("data").get("高频头"))              
            tuner_str = "".join(tuner_list) if tuner_list else ""
            self._logger.info("高频头：" + str(tuner_str))
        else:
            tuner_str = ''
        return tuner_str

    def get_task_type(self):
        task_type_list = list()
        task_type_list.append(self.Ltcresponsejson.get("data").get("分类"))             
        if task_type_list:
            task_type_str = task_type_list[0].strip().strip('\r\n')
            if task_type_str:
                self._logger.info("任务类型：" + task_type_str)
                return task_type_str
            else:
                return ""
        else:
            return ""

    def get_task_stage(self):
        task_stage_xpath = \
            '//th[contains(text(),"任务阶段")]/../../tr[2]/td[2]/div/text()'
        task_stage_list = self.html.xpath(task_stage_xpath)
        if task_stage_list:
            task_stage_str = task_stage_list[0].strip().strip('\r\n')
            if task_stage_str:
                self._logger.info("任务阶段：" + task_stage_str)
                return task_stage_str
            else:
                return ""
        else:
            return ""

    def get_customer_batch_code(self):
        product_str = self.Ltcresponsejson.get("data").get("客户批号")
        if product_str:
            product_str = product_str.strip().strip('\r\n')
            if product_str:
                self._logger.info("客户批号：" + product_str)
                return product_str
            else:
                return ""
        else:
            return ""

    def get_xml_attach_id(self):
        xml_attach_id_xpath = \
            'descendant::*[@class="load_fw_comfirm"]'
        xml_attach_id_list = self.html.xpath(xml_attach_id_xpath)
        if xml_attach_id_list:
            xml_attach_id = xml_attach_id_list[0].get("xml_attach_id")
            if xml_attach_id:
                self._logger.info("xml_attach_id：" + xml_attach_id)
                return xml_attach_id
            else:
                return ""
        else:
            return ""


    def get_order_status_type(self):
        product_xpath = \
            '//th[contains(text(),"任务状态")]/../td/div/text()'
        product_list = self.html.xpath(product_xpath)
        if product_list:
            product_str = product_list[0].strip().strip('\r\n')
            if product_str:
                self._logger.info("任务状态：" + product_str)
                return product_str
            else:
                return ""
        else:
            return ""


    def get_wifi_bluetooth(self):
        if self.Ltcresponsejson.get("data").get("WIFI与蓝牙") != None:
            wifi_bluetooth_str = ''
            wifi_bluetooth_list = list()
            wifi_bluetooth_list.append(self.Ltcresponsejson.get("data").get("WIFI与蓝牙"))           
            wifi_bluetooth_str += "".join(wifi_bluetooth_list).strip() if wifi_bluetooth_list else ""
            wifi_str = "".join(wifi_bluetooth_str).strip() if wifi_bluetooth_str else ""
        else:
            wifi_str = ''
        return wifi_str

    def get_wifi_bluetooth_info(self):
        if self.Ltcresponsejson.get("data").get("WIFI与蓝牙") != None:
            wifi_bluetooth_str = ''
            wifi_bluetooth_list = list()
            wifi_bluetooth_list.append(self.Ltcresponsejson.get("data").get("WIFI与蓝牙"))           
            wifi_bluetooth_str += "".join(wifi_bluetooth_list).strip() if wifi_bluetooth_list else ""
            wifi_str = "".join(wifi_bluetooth_str).strip() if wifi_bluetooth_str else ""
        else:
            wifi_str = ''
        return wifi_str

    def get_choose_ci(self):
        choose_list = list()
        if self.Ltcresponsejson.get("data").get("可选功能") !=None:
            choose_list.append(self.Ltcresponsejson.get("data").get("可选功能"))           
            # CI
            ci_str = 'CI' if 'CI' in "".join(choose_list).strip() else ""
        else:
            ci_str=''
        self._logger.info("可选功能CI类型：" + str(ci_str))
        return ci_str

    def get_choose_wifi(self):
        choose_xpath = \
            '//*[@id="orderinfo_hw"]//th[contains(text(),"可选功能")]/../td/strong/text()'
        choose_list = self.html.xpath(choose_xpath)
        wifi_module_str = ""
        if '内置WIFI模块' in "".join(choose_list).strip():
            wifi_module_xpath_1 = \
                '//*[@id="orderinfo_hw"]//th[contains(text(),"可选功能")]/../td/strong/text()'
            wifi_module_list_1 = self.html.xpath(wifi_module_xpath_1)
            wifi_module_str += "".join(wifi_module_list_1).strip() if wifi_module_list_1 else ""
            wifi_module_xpath = \
                '//*[@id="orderinfo_hw"]//th[contains(text(),"可选功能")]/../td/p/text()'
            wifi_module_list = self.html.xpath(wifi_module_xpath)
            wifi_module_str += "".join(wifi_module_list[0]).strip() if wifi_module_list else ""
            self._logger.info("可选功能WIFI模块：" + wifi_module_str)
            return wifi_module_str
        else:
            return ""

    def get_customer_special_requirement(self):
        customer_special_requirement_list = list()
        customer_special_requirement_list.append(self.Ltcresponsejson.get("data").get("客户特殊需求"))           
        customer_special_requirement_str = "".join(customer_special_requirement_list).strip('\n').strip() if customer_special_requirement_list else ""
        self._logger.info("客户特殊需求：" + customer_special_requirement_str)
        return customer_special_requirement_str

    def get_option_func(self):
        if self.Ltcresponsejson.get("data").get("可选功能") != None:
            option_list = list()
            option_list.append(self.Ltcresponsejson.get("data").get("可选功能"))          
            option_str = "".join(option_list).strip() if option_list else ""
        else:
            option_str = ''           
        return option_str

    def get_tv_system(self):
        if self.order_type == self.FORMAL_ORDER:
            if self.Ltcresponsejson.get("data").get("可选功能") != None:
                tvsystem_list = list()
                tvsystem_list.append(self.Ltcresponsejson.get("data").get("可选功能"))            
                tvsystem_str = "".join(tvsystem_list).strip() if tvsystem_list else ""
                tvsystem_str = "" if tvsystem_str == '无' else tvsystem_str
                self._logger.info("电视制式：" + str(tvsystem_str))
            else:
                tvsystem_str = ''                
            return tvsystem_str
        else:
            return ""

    def get_ddr_info(self):
        ddr_info_list = list()
        ddr_info_list.append(self.Ltcresponsejson.get("data").get("External DDR"))            
        ddr_info_str = "" if ddr_info_list == [] else "".join('%s' % id for id in ddr_info_list)
        if "}{" in ddr_info_str:
            i = 0
            ddr_info_list = ddr_info_str.split('}{')
            for info in ddr_info_list:
                ddr_info_list[i] = info.replace("refDec", "refDec" + str(i)).replace("supplierNo", "supplierNo" + str(i)).replace("itemNo", "itemNo" + str(i)).replace("categoryDescp", "categoryDescp" + str(i)).replace("capacity", "capacity" + str(i))
                i = i + 1
            ddr_info_str = ','.join(ddr_info_list)
            ddr_info_str = ddr_info_str.replace("refDec0", "refDec").replace("supplierNo0", "supplierNo").replace("itemNo0", "itemNo").replace("categoryDescp0", "categoryDescp").replace("capacity0", "capacity")
        return ddr_info_str

    def get_task_comment_area(self):
        url = 'http://ocs-api.gz.cvte.cn/tv/TaskComments/get_all_task_comments_json/?task_id=' + self.ocs_number + '&order=DESC'
        response = PyocsRequest().pyocs_request_get(url)
        soup = bs4.BeautifulSoup(response.content.decode("unicode–escape"), "lxml")
        task_comment_str = str(soup)
        return task_comment_str

    def get_produce_batch_code(self):
        batch_code_str = ''
        batch_code_str = (self.Ltcresponsejson.get("data").get("生产批次"))           
        batch_code_str = batch_code_str.strip().strip('\r\n')
        self._logger.info("生产批号：", batch_code_str)
        # still not right now ,json from ltc wrong
        return batch_code_str

    def get_software_tracker(self):
        if self.order_type == self.FORMAL_ORDER:
            t_xpath = '//*[@id="basicinfo_region"]//*[@id="Task__sw_track_user_id_history"]/../span/text()'
            t_list = self.html.xpath(t_xpath)
            t_str = "".join(t_list[0]).strip() if t_list else ""  # 删除开头与结尾的空白符（包括'\n', '\r',  '\t',  ' ')
            self._logger.info("软件跟踪人员：" + str(t_str))
            return t_str
        else:
            return ""
    def get_software_audit(self):
        if self.order_type == self.FORMAL_ORDER:
            t_xpath = '//*[@id="basicinfo_region"]//*[@id="Task__sw_audit_user_id_history"]/../span/text()'
            t_list = self.html.xpath(t_xpath)
            t_str = "".join(t_list[0]).strip() if t_list else ""  # 删除开头与结尾的空白符（包括'\n', '\r',  '\t',  ' ')
            self._logger.info("软件审核人员：" + str(t_str))
            return t_str
        else:
            return ""

    def get_opm(self):
        opm_xpath = \
            '//th[contains(text(),"高级经理")]/../td/text()'
        opm_list = self.html.xpath(opm_xpath)
        if opm_list:
            opm_str = opm_list[0].strip().strip('\r\n')
            if opm_str:
                self._logger.info("高级经理：" + opm_str)
                return opm_str
            else:
                return ""
        else:
            return ""

    def get_nq(self):
        nq_xpath = \
            '//th[contains(text(),"负责内勤")]/../td/text()'
        nq_list = self.html.xpath(nq_xpath)
        if nq_list:
            nq_str = nq_list[0].strip().strip('\r\n')
            if nq_str:
                self._logger.info("负责内勤：" + nq_str)
                return nq_str
            else:
                return ""
        else:
            return ""

    def get_ebs_num(self):
        ebs_xpath = \
            '//th[contains(text(),"EBS订单编号")]/../td/text()'
        ebs_list = self.html.xpath(ebs_xpath)
        if ebs_list:
            ebs_str = ebs_list[0].strip().strip('\r\n')
            if ebs_str:
                self._logger.info("EBS订单编号" + ebs_str)
                return ebs_str
            else:
                return ""
        else:
            return ""

    def get_sw_branch_path(self):
        """
        if self.order_type == self.FORMAL_ORDER:
            sw_branch_xpath = \
                '//th[contains(text(),"分支量产状态")]/../td/text()'
            sw_branch_list = self.html.xpath(sw_branch_xpath)
            sw_branch_str = "".join(sw_branch_list).strip().strip('\r\n') if sw_branch_list else ""
            sw_branch_str = sw_branch_str if sw_branch_str else ""
            self._logger.info("分支量产状态：" + str(sw_branch_str))
            return sw_branch_str
        elif self.order_type == self.SAMPLE_ORDER:
            return ""
        else:
            return ""
        """
        return ""

    def get_os_system(self):
        system_list = list()
        system_list.append(self.Ltcresponsejson.get("data").get("OS系统"))            
        system_str = "".join(system_list).strip() if system_list else ""
        system_str = "" if system_str == '无' else system_str
        self._logger.info("OS系统：" + str(system_str))
        return system_str

    def get_request(self):
        """
        # 返回：字典
        # 包含内容（eg）：
        # {'产品型号': 'TP.MS3663T.PB707'
        # '主芯片': 'MSD3666LSAT-U9-广东海信-客供(DD;DD+;RMVB)',
        # 'FlashSize': '8MByte',
        # '子板型': 'PB707_A3',
        # 'ddrSize': '',
        # '可选功能': '无',
        # '区域': '菲律宾',
        # 'CI PLUS功能': '无',
        # '占空比': '70'
        # ...
        #
        # }
        """
        request_dict = dict()
        # 产品型号
        request_dict[self.product_name] = self.get_product_name()
        # 主芯片
        request_dict[self.chip_name] = self.get_chip_name()

        # flash size
        request_dict[self.flash_size_name] = self.get_flash_size()
        # flash信息
        request_dict[self.flash_info] = self.get_flash_info()
        # 子板型
        request_dict[self.port_name] = self.get_port_name()
        # 板卡端子信息
        request_dict[self.port_info] = self.get_port_info()
        # DDR
        
        request_dict[self.ddr_name] = self.get_ddr_size()
        # 可选功能
        request_dict[self.ci_type] = self.get_choose_ci()
        # WIFI模块
        request_dict[self.wifi_module_info] = self.get_wifi_bluetooth()
        # 区域
        request_dict[self.region_name] = self.get_region_name()
        # CI Plus
        request_dict[self.ciplus_name] = self.get_ci_plus()
        # 占空比
        request_dict[self.pwm_name] = self.get_pwm()
        # 高频头
        request_dict[self.tuner_name] = self.get_tuner_type()
        # 客户批号
        request_dict[self.customer_batch_code] = self.get_customer_batch_code()
        # 客户机型
        request_dict[self.customer_machine] = self.get_customer_machine()
        # 其它应用软件
        request_dict[self.other_app_soft] = self.get_other_app_software()
        # WIFI与蓝牙
        request_dict[self.wifi_bluetooth_type] = self.get_wifi_bluetooth()
        # WIFI与蓝牙信息
        request_dict[self.wifi_bluetooth_info] = self.get_wifi_bluetooth_info()
        # 主芯片备注
        request_dict[self.chip_remark] = self.get_chip_remark()
        # 客户特殊需求
        request_dict[self.customer_special_requirement] = self.get_customer_special_requirement()
        # 可选功能
        request_dict[self.option_func] = self.get_option_func()
        # 电视制式
        request_dict[self.tv_system] = self.get_tv_system()
        # 存储器信息
        request_dict[self.ddr_info] = self.get_ddr_info()
        # 分支量产状态
        request_dict[self.sw_branch_path] = self.get_sw_branch_path()
        # OS系统
        request_dict[self.os_system] = self.get_os_system()

        return request_dict

    def get_number_by_product_batch_code(self, batch_code):
        product_number_xpath = '//th[contains(text(),"生产数量")]/../td/text()'
        search_form_data = dict()
        search_form_data["data[link_id]"] = batch_code
        search_response = PyocsRequest().pyocs_request_post("http://ocs-api.gz.cvte.cn/tv/Tasks", data=search_form_data, allow_redirects=True)
        html = etree.HTML(search_response.text)
        product_number_list = html.xpath(product_number_xpath)
        if product_number_list:
            product_number_str = product_number_list[0].strip().strip('\r\n')
            if product_number_str:
                self._logger.info("生产数量：" + product_number_str)
                return product_number_str
            else:
                return ""
        else:
            return ""

    def is_audit_failed(self, sw_name):
        prefix = '//a[contains(text(), "'
        postfix = '")]'
        path = prefix + sw_name + postfix
        audit_status_path = path + "//ancestor::td//preceding::td[2]//a[2]/span"
        res = self.html.xpath(audit_status_path)
        if res:
            return res[0].text == '自动审核失败'
        self._logger.info('获取审核状态失败')

    def get_product_name_and_version(self):
        product_xpath = \
            '//h5[contains(text(),"硬件需求")]/..//strong/a/text()'
        product_list = self.html.xpath(product_xpath)
        product_str = "".join(product_list).strip().strip('\r\n') 
        self._logger.info("产品型号：" + str(product_str))
        return product_str

    def get_plan_end_date(self):
        plan_end_xpath = '//a[@field="Task__plan_end_date"]/..//span/text()'
        plan_end_list = self.html.xpath(plan_end_xpath)
        plan_end_str= "".join(plan_end_list).strip().strip('\r\n') 
        self._logger.info("计划完成日期：" + str(plan_end_str))
        return plan_end_str

    def get_all_produce_batch_code(self):
        batch_code_str = ''
        batch_code_str = (self.Ltcresponsejson.get("data").get("生产批次"))           
        batch_code_str = batch_code_str.strip().strip('\r\n')
        self._logger.info("生产批号：", batch_code_str)
        # still not right now ,json from ltc wrong
        return batch_code_str