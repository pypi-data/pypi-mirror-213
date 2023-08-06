from projectRule.mt9255.MT9255Common import MT9255Common
from pyocs.pyocs_exception import *


class Ruler(MT9255Common):

    # Customer_ID
    _customer_id = 'CUSTOMER_SAMPLE_AUTO_CONFIG'

    # 代码分支
    _code_branch = ''

    # 测试类型
    _test_type = 'F'

    # 安卓系统
    _android_system = ''

    def get_ocs_modelid(self):
        project = self.request_dict[self.ocs_demand.product_name].replace('.', '_')
        modelid = 'CS' + self.ocs_number + '_SAMPLE_' + project + '_ID_PNL_GENERAL_1366_768' \
                  + '_DUTY_' + self.request_dict[self.ocs_demand.pwm_name]
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
        ret += '#elif ( IsModelID('+ self.get_ocs_modelid() + ') )' + '\n'
        ret += '// board & chip & Flash & pwm' + '\n'
        ret += self.get_board_macro()
        ret += self.get_chip_macro()
        ret += self.get_flash_size_macro()
        ret += self.get_bluetooth_macro()
        ret += self.get_pwm_macro()

        # 因为对于样品订单来说不需要关注遥控器/按键板/logo等的配置项，如果写客户订单的处理逻辑，需要注意这些配置项
        ret += '//ir & keypad & logo' + '\n'
        ret += '#define CVT_DEF_IR_TYPE'.ljust(_space) + 'ID_IR_CVTE_AM_KA80' + '\n'
        ret += '#define CVT_DEF_KEYPAD_TYPE'.ljust(_space) + 'ID_KEYPAD_CVTE_7KEY_COMMON_DEFAULT' + '\n'
        ret += '#define CVT_DEF_KEYPAD_ADC'.ljust(_space) + 'ID_KEYPAD_ADC_COMMON_DEFAULT' + '\n'
        ret += '#define CVT_DEF_LOGO_TYPE'.ljust(_space) + 'ID_LOGO_CVT_OVERSEAS_COMMON_DEFAULT' + '\n'

        # 样品订单不需要关注屏幕信息，如果写客户订单的处理逻辑，需要注意
        ret += '#define CVT_DEF_PANEL_TYPE'.ljust(_space) + 'ID_PNL_GENERAL_1366_768' + '\n'

        ret += '//country & language' + '\n'
        ret += '#define CVT_DEF_COUNTRY_SELECT'.ljust(_space) + 'ID_COUNTRY_INDIA' + '\n'
        ret += '#define CVT_DEF_LANGUAGE_SELECT'.ljust(_space) + 'ID_LANGUAGE_ENGLISH' + '\n'
        ret += '//launcher' + '\n'
        ret += '#define CVT_DEF_LAUNCHER_TYPE'.ljust(_space) + 'ID_LAUNCHER_40_NON_GAIA_SPACE4' + '\n'

        ret += '//END\n'
        return ret

    def get_code_branch(self):
        self._code_branch = 'fae_all'
        return self._code_branch
