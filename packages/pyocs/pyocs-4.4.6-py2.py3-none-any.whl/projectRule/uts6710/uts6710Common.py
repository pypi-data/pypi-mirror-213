import abc
from pyocs.pyocs_interface import UniteInterface


class Uts6710Common(UniteInterface):

    def get_board_macro(self):
        product_split_list = self.request_dict[self.ocs_demand.product_name].split('.')
        board_platform = product_split_list[1]
        board_type = product_split_list[2]
        sub_board_split_list = self.request_dict[self.ocs_demand.port_name].split('_')
        sub_board_type = sub_board_split_list[1]

        if "SK105A" in board_platform:
            board_macro = "ID_BD_SK105A_" + board_type + "_SUB_" + sub_board_type
        elif "US6710" in board_platform:
            board_macro = "ID_BD_US6710_" + board_type + "_SUB_" + sub_board_type
        else:
            raise RuntimeError('此板型没有录入，请补充')
        ret = "#define CVT_DEF_BOARD_TYPE".ljust(self._space) + board_macro + '\n'
        return ret

    def get_chip_macro(self):
        chip_type_list = self.request_dict[self.ocs_demand.chip_name].split('(')
        chip_type = chip_type_list[0]
        if 'UTS6710-D' in chip_type:
            chip_type = 'ID_CHIP_UTS6710_D'
        elif 'UTS6710-X' in chip_type:
            chip_type = 'ID_CHIP_UTS6710_X'
        elif 'UTS6710W-D' in chip_type:
            chip_type = 'ID_CHIP_UTS6710W_D'
        elif 'UTS6710W-X' in chip_type:
            chip_type = 'ID_CHIP_UTS6710W_X'
        else:
            raise RuntimeError('此芯片型号没有录入，请补充')
        chip_macro = chip_type
        ret = "#define CVT_DEF_CHIP_TYPE".ljust(self._space) + chip_macro + '\n'
        return ret

    def get_dolby_macro(self):
        pass

    def get_flash_size_macro(self):
        flash_size = self.request_dict[self.ocs_demand.flash_size_name]
        if '8M' in flash_size:
            flash_size_id = 'ID_FLASH_8M'
        elif '4M' in flash_size:
            flash_size_id = 'ID_FLASH_4M'
        else:
            raise RuntimeError('此flash没有录入，请补充')
        ret = "#define CVT_DEF_FLASH_SIZE".ljust(self._space) + flash_size_id + '\n'
        return ret

    def get_pwm_macro(self):
        pwm_macro = self.request_dict[self.ocs_demand.pwm_name]
        ret = "#define CVT_DEF_CURRENT_REF_DUTY".ljust(self._space) + pwm_macro + '\n'
        return ret

    def get_eshare_macro(self):
        pass

    def get_code_branch(self):
        return self._code_branch

    def get_dc_voltage_detect_macro(self):
        port_type_str = self.request_dict[self.ocs_demand.port_name]
        customer_special_requirement_str = self.request_dict[self.ocs_demand.customer_special_requirement]
        if "增加高压、低压保护电路（低压保护点11V，高压保护点14V）" in customer_special_requirement_str or \
                "DC/9.5V-18V从电源端子输入，增加高压、低压保护电路（低压保护点9.5V，高压保护点18V）" in customer_special_requirement_str or \
                "DC/12V从电源端子输入，增加高压、低压保护电路（低压保护点10.8V，高压保护点13.5V）" in customer_special_requirement_str or \
                "增加高压、低压保护电路（低压保护点11V，高压保护点13.5V）" in customer_special_requirement_str or \
                "增加高压、低压保护电路（DC输入电压范围11V~13.5V）" in customer_special_requirement_str or \
                "增加高压、低压保护电路（DC输入电压范围11V~13.5V）" in customer_special_requirement_str:
            ret = "#define CVT_EN_DC_VOLTAGE_VALUE_DETECT".ljust(self._space) + '1' + '\n'
        else:
            if 'PB824' in port_type_str or 'PB817' in port_type_str or 'PA673' in port_type_str or 'PA672' in port_type_str:
                ret = "#define CVT_EN_DC_VOLTAGE_VALUE_DETECT".ljust(self._space) + '0' + '\n'
            else:
                ret = ''
        return ret

    def get_dc_voltage_low_value_macro(self):
        port_type_str = self.request_dict[self.ocs_demand.port_name]
        customer_special_requirement_str = self.request_dict[self.ocs_demand.customer_special_requirement]
        if 'PB824' in port_type_str and "增加高压、低压保护电路（低压保护点11V，高压保护点14V）" in customer_special_requirement_str:
            ret = "#define CVT_DEF_LOW_VALUE_IN_VOLTAGE_PROTECT".ljust(self._space) + '147' + '\n'
        elif 'PB817' in port_type_str:
            if "DC/9.5V-18V从电源端子输入，增加高压、低压保护电路（低压保护点9.5V，高压保护点18V）" in customer_special_requirement_str:
                ret = "#define CVT_DEF_LOW_VALUE_IN_VOLTAGE_PROTECT".ljust(self._space) + '130' + '\n'
            elif "DC/12V从电源端子输入，增加高压、低压保护电路（低压保护点10.8V，高压保护点13.5V）" in customer_special_requirement_str:
                ret = "#define CVT_DEF_LOW_VALUE_IN_VOLTAGE_PROTECT".ljust(self._space) + '138' + '\n'
            elif "DC/12V从电源端子输入，增加高压、低压保护电路（低压保护点11V，高压保护点13.5V）" in customer_special_requirement_str:
                ret = "#define CVT_DEF_LOW_VALUE_IN_VOLTAGE_PROTECT".ljust(self._space) + '147' + '\n'
            else:
                ret = ''
        else:
            ret = ''
        return ret

    @abc.abstractmethod
    def get_ocs_modelid(self):
        pass

    @abc.abstractmethod
    def get_ocs_require(self):
        pass
