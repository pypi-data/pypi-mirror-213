from projectRule.uts6710.uts6710Common import Uts6710Common
import re

class Ruler(Uts6710Common):

    # Customer_ID
    _customer_id = 'CUSTOMER_JINPIN'

    # 代码分支
    _code_branch = 'fae_v56'

    # 测试类型
    _test_type = 'E'

    def get_board_macro(self):
        product_split_list = self.request_dict[self.ocs_demand.product_name].split('.')
        board_platform = product_split_list[1]
        board_type = product_split_list[2]
        sub_board_split_list = self.request_dict[self.ocs_demand.port_name].split('_')
        sub_board_type = sub_board_split_list[1]

        if "SK105A" in board_platform:
            if "PB815" in board_type:
                board_macro = "ID_BD_SK105A_" + board_type +"B"+ "_SUB_" + sub_board_type
            else:
                board_macro = "ID_BD_SK105A_" + board_type + "_SUB_" + sub_board_type
        elif "US6710" in board_platform:
            board_macro = "ID_BD_US6710_" + board_type + "_SUB_" + sub_board_type
        else:
            raise RuntimeError('此板型没有录入，请补充')
        ret = "#define CVT_DEF_BOARD_TYPE".ljust(self._space) + board_macro + '\n'
        return ret

    def get_ocs_modelid(self):
        project = self.request_dict[self.ocs_demand.product_name].replace('.', '_')
        if "PB815" in project:
            project = project +"B"       
        batch_code = self.request_dict[self.ocs_demand.customer_batch_code]
        batch_code = re.sub("\D|'-'", "", batch_code)
        if not batch_code:
            batch_code = '01000001001'
        else:
            batch_code = batch_code.replace('-', '_')
        machine = self.request_dict[self.ocs_demand.customer_machine]
        machine = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", '', machine)
        if not machine:
            machine = 'X00XX0000'
        else:
            machine = machine.replace('.', '_')
        modelid = 'CP' + self.ocs_number + '_AC_JPE_' + project + '_LC390TA2A_0' + '_BLUE_' + batch_code + '_' + machine
        return modelid

    def get_ocs_require(self):
        """获取ocs上的配置，生成配置代码
        Args:
            ocs_number：OCS订单号
        Returns:
             返回配置代码
        """
        ret = ''
        _space = 60
        ret += '#elif ( IsModelID(' + self.get_ocs_modelid() + ') )' + '\n'
        ret += '// hardware' + '\n'
        # 主板宏
        ret += self.get_board_macro()
        ret += self.get_chip_macro()
        ret += self.get_flash_size_macro()
        # 客户特殊需求
        ret += self.get_dc_voltage_detect_macro()
        ret += self.get_dc_voltage_low_value_macro()
        # Pwm占空比宏：[占空比：60]
        ret += self.get_pwm_macro()

        # 金品代测订单不需要关注IR/KEYPAD/LOGO等的配置项
        ret += '// ir & keypad & logo' + '\n'
        ret += '#define CVT_DEF_IR_TYPE'.ljust(_space) + 'ID_IR_JP_AP_RS22_CN_EXIT' + '\n'
        ret += '#define CVT_DEF_LOGO_TYPE'.ljust(_space) + 'ID_LOGO_JPE_BLUE' + '\n'

        # 金品代测订单不需要关注PANEL
        ret += '// panel id' + '\n'
        ret += '#define CVT_DEF_PANEL_TYPE'.ljust(_space) + 'ID_PNL_GENERAL_1366_768' + '\n'
        ret += '#define CVT_DEF_PQ_TYPE'.ljust(_space) + 'ID_PQ_JPE_LC390TA2A_CS695356' + '\n'

        ret += '// brand id' + '\n'
        ret += '#define CUSTOMER_MODE'.ljust(_space) + 'CUSTOMER_MODE_COMMON' + '\n'

        ret += '// end\n'
        return ret


















