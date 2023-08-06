
    def get_all_software_info_from_html(self, html, exclude_bin=True):
        """获取订单上的启用状态下的软件以及对应的信息字典
        Args:
            html: 某个ocs订单的html页面
        Returns:
            启用状态下的非烧录 bin 或者不符合 CVTE 规范的软件以及对应的信息字典
        """
        sw_name_list = []
        software_info_list = []
        #获取的是文件不是软件
        sw_name_list = html.xpath('//div[@id="file_names"]/p/text()')

        self._logger.info("所有的软件:" + str(sw_name_list))

        for sw_name in sw_name_list:
            #if not PyocsSoftware().is_sw_locked(sw_name=sw_name, html=html):
            if exclude_bin and self.is_burn_bin(sw_name=sw_name):
                continue
            if exclude_bin and not self.is_cvte_spec_sw(sw_name=sw_name):
                continue
            software_info_list = html.xpath('//*[text()=$val]/../following-sibling::td[5]/text()', val=str(sw_name))
            print("software_info_list",software_info_list)
            sw_info = ','.join(software_info_list)
            sw_name_list.append(sw_name)
            software_info_list.append(sw_info)

        enable_software_dict = dict(zip(sw_name_list, software_info_list))
        return enable_software_dict

    def upload_old_sw_by_id(self, ocs_num, old_sw_id, burn_place_hold, burn_type, disable_origin_sw=True):
        """根据ocs_num 和old_sw_name， 上传库存软件
        """
        fields = {'data[fw_Attach][file][]': '(binary)',
                  'data[fw_Attach][old_fw_id][]': str(old_sw_id),
                  'data[fw_Attach][ab_sw_name][]': '',
                  'data[fw_Attach][ab_sw_id][]': '',
                  'data[fw_Attach][ab_xml_name][]': '',
                  'data[fw_Attach][ab_xml_id][]': '',
                  'data[fw_Attach][autobuild_bill_no][]': '',
                  'data[fw_Attach][fileXML][]': '(binary)',
                  'data[fw_Attach][test_type][]': "100",  # 默认不用测试
                  'data[fw_Attach][fw_cfm_type]': '',
                  'data[fw_Attach][soft_remark]': '',
                  'data[fw_Attach][burn_place_hold][]': burn_place_hold,
                  'data[fw_Attach][burn_type]': burn_type,
                  'data[fw_Attach][function_description]': '',
                  'data[fw_Attach][result_of_modified]': '',
                  'data[fw_Attach][note][]': "引用库存软件",
                  'data[change_task_status]': 'on'
                  }
        if disable_origin_sw:
            sw_list = PyocsSoftware().get_enable_software_list(ocs_number=ocs_num, exclude_bin=False)
            if sw_list:
                for sw in sw_list:
                    print('sw',sw)
                    fields.update({'data[fw_Attach][fileList][' + sw.attachment_id + ']': 'on'})
                    print('fields',fields)
            print('sw_list',sw_list)
        print('final_fields',fields)
        ret = PyocsRequest().pyocs_request_post(self._upload_fw_url_prefix + str(ocs_num), data=fields)
        return ret.status_code == 200



    def find_old_sw_list_by_name(self, old_sw_name):
        """根据 old_sw_name 查找库存软件 old_sw_id
        Args:
            old_sw_name: 软件名
        Returns:
            查找到的软件字典
        """
        old_sw_dict = dict()
        self._logger.info(old_sw_name)
        data = {
            'data[autocomplete]': str(old_sw_name)
        }
        search_response = PyocsRequest().pyocs_request_post(self._ocs_find_old_sw_url, data=data, allow_redirects=True)
        html = etree.HTML(search_response.text)
        old_sw_id_str_list = html.xpath('//div[@class="clearfix"]//input/@value')
        sw_name_list = html.xpath('//td[@class="FirmwareAttachment_col_attachment_id  MainField"]/text()')
        self._logger.info("ocs old_sw_id_str_list" + str(old_sw_id_str_list))
        self._logger.info("ocs sw_name_list" + str(sw_name_list))
        if old_sw_id_str_list and sw_name_list:
            old_sw_dict = dict(zip(old_sw_id_str_list, sw_name_list))
        self._logger.info("ocs 库存软件查找：" + str(old_sw_dict))
        return sw_name_list



    #根据fw_id，上传指定的fw_id到目标ocs
    def reuse_old_sw_from_src_to_dst_by_id(self, src_ocs, old_sw_name, dst_ocs, workspace):
        """
        引用库存软件，如果此单上已经引用了同名的库存软件，则不做引用
        :param src_ocs:
        :param dst_ocs:
        :return:
        """
        dst_ocs_sw_name_list = []
        reuse_sw_name_list = []
        old_sw_name = ""
        sw_reuse_burn_type = {'在线烧录': '1', '离线烧录': '2'}

        src_ocs_link = self._ocs_link_Prefix + src_ocs
        response = PyocsRequest().pyocs_request_get(src_ocs_link)
        html = etree.HTML(response.text)

        dst_ocs_sw_list = PyocsSoftware().get_enable_software_list(ocs_number=dst_ocs, exclude_bin=False)
        if dst_ocs_sw_list:
            for dst_ocs_sw in dst_ocs_sw_list:
                # OCS系统的逆天bug，可能会出现两单相同软件，但是其中一个字母一边大写一边小写，此处为了这个bug，统一采用大写比较
                dst_ocs_sw_name_list.append(str(dst_ocs_sw.name.upper()))
        sw_list = PyocsSoftware().get_enable_software_list(ocs_number=src_ocs, exclude_bin=False)        
        sw_dict = self.get_all_software_info_from_html(html, exclude_bin=False)
        print("hello")
        if not sw_list:
            raise NoSoftwareError("源订单上无可用软件")
        #all_sw_list = get_all_software_list_from_html
        sw_list = find_old_sw_id_by_name(old_sw_name)
        for index, sw in enumerate(reversed(sw_list)):
            if str(sw.name).upper() not in dst_ocs_sw_name_list:
                # 如果库存软件包含烧录位号信息，同步引用该信息；否则，根据dst订单自带的烧录位号信息设置
                burn_info = sw_dict[sw.name]
                if burn_info:
                    burn_place_hold = burn_info.split(",")[0]
                    burn_type = sw_reuse_burn_type[burn_info.split(",")[1]]
                else:
                    ddr_info_str = PyocsDemand(src_ocs).get_ddr_info()
                    ddr_info_dict = eval(ddr_info_str)
                    flash_list1 = ['EMMC FLASH', 'NAND FLASH']
                    flash_list2 = ['NOR FLASH']
                    burn_place_hold_nums = ddr_info_str.count('refDec')
                    burn_place_hold_itemNo = ddr_info_dict['categoryDescp']
                    if 1 == burn_place_hold_nums and ddr_info_dict['refDec'] is not None:
                        burn_place_hold = ddr_info_dict['refDec']
                        if burn_place_hold_itemNo in flash_list1:
                            burn_type = self.sw_burn_type["在线烧录"]
                        elif burn_place_hold_itemNo in flash_list2:
                            burn_type = self.sw_burn_type["离线烧录"]
                    else:
                        burn_place_hold = ' '
                        burn_type = ' '
                self.upload_old_sw_by_id(ocs_num=dst_ocs, old_sw_id=sw.fw_id, burn_place_hold=burn_place_hold, burn_type=burn_type, disable_origin_sw=(index == 0))
                reuse_sw_name_list.append(sw.name)
        if not reuse_sw_name_list:
            return True
        while reuse_sw_name_list[-1] \
                not in PyocsSoftware().get_enable_software_list_from_html(PyocsDemand(ocs_number=dst_ocs).get_ocs_html()):
            continue






do_daice_task = atuo_do_daice_sw()   
old_sw_name = "CP549931_JPE_TP_MS3663S_PB801_MALAYSIA_PT320AT01_5_BLUE_01202005282_E40DM1100_8MB_REF77_AT_R_0x60D0_20200608_015125.tar "
do_daice_task.reuse_old_sw_from_src_to_dst_by_id('562404',old_sw_name,'567172', os.getcwd())
"""