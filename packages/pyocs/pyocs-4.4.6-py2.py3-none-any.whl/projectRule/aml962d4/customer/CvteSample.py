from projectRule.aml962d4.Aml962d4Common import Aml962d4Common
from customers.customer_common.common_database import commonDataBase
from pyocs import faas_api
import json

class Ruler(Aml962d4Common):

    # Customer_ID
    _customer_id = 'CUSTOMER_SAMPLE_SELF'

    # 代码分支
    _code_branch = ""

    # 测试类型
    _test_type = 'F'

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
        body["方案"] = self.ocs_demand.get_ocs_project_name()
        body["分支"] = self.get_code_branch()
        body["customer_id"] = self._customer_id
        body["ddrSize"] = self.ocs_demand.get_ddr_size()
        body.update(self.ocs_demand.Ltcresponsejson['data'])

        gpt_macro = faas_api.get_gpt_config_sample_order(body)

        if gpt_macro:
            ret += gpt_macro
            return ret

