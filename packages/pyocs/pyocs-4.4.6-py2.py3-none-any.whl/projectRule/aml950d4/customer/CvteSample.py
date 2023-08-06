from projectRule.aml950d4.Aml950d4Common import Aml950d4Common
from customers.customer_common.common_database import commonDataBase
from pyocs import faas_api
import json

class Ruler(Aml950d4Common):

    # Customer_ID
    _customer_id = 'CUSTOMER_SAMPLE_SELF'

    # 代码分支
    _code_branch = ""

    # 测试类型
    _test_type = 'F'

    android_13 = 'AN13'

    def get_ocs_modelid(self):
        project = self.request_dict[self.ocs_demand.product_name].replace('.', '_')
        modelid = 'CS' + self.ocs_number + '_SAMPLE_' + project + '_ID_PNL_GENERAL' \
                  + '_DUTY_' + self.request_dict[self.ocs_demand.pwm_name]
        return modelid

    def get_ocs_require(self):
        """获取ocs上的配置，生成配置代码
        Args:
            ocs_number：OCS订单号
        Returns:
             返回配置代码
        """
        ret = '#elif ( IsModelID(' + self.get_ocs_modelid() + ') )\n'

        body = {}
        body["方案"] = "T950D4_AN13" #self.ocs_demand.get_ocs_project_name()
        body["分支"] = self.get_code_branch()
        body["customer_id"] = "CUSTOMER_SAMPLE_SELF" #self._customer_id
        body["ddrSize"] = self.ocs_demand.get_ddr_size()
        body.update(self.ocs_demand.Ltcresponsejson['data'])

        ret += faas_api.get_gpt_config_sample_order(body)

        return ret

    def get_android_system(self):
        if "Android13" in self.ocs_demand.get_customer_special_requirement():
            return self.android_13

    def get_ocs_country(self):
        ret = ''
        ret += self.get_macro_line("CVT_DEF_COUNTRY_SELECT", "ID_COUNTRY_TURKEY")
        return ret