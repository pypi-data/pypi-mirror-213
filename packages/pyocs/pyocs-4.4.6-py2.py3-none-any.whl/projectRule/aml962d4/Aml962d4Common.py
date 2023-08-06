import abc
from pyocs.pyocs_interface import UniteInterface
from customers.customer_common.common_database import commonDataBase
from pyocs.pyocs_exception import *


class Aml962d4Common(UniteInterface):

    def get_code_branch(self):
        region_name_list = self.request_dict[self.ocs_demand.region_name]
        if not region_name_list:
            raise NoRegionError('此单无区域')
        map_list = commonDataBase().get_region_mapping_info_by_country(region_name_list)
        tv_system_str = map_list[0]
        country_region_str = map_list[1]
        if not tv_system_str:
            raise OcsRegionError('无法查询到此区域的制式')
        if 'ATV' in tv_system_str:
            if country_region_str == '欧洲':
                self._code_branch = 'fae_962D4'
            else:
                raise RuntimeError('该国家不属于区域支持所属范围，请确认，谢谢！')
        elif 'DVB' in tv_system_str:
            self._code_branch = 'fae_962D4'
        else:
            raise RuntimeError('该方案不支持此制式，或者检查该国家制式是否正确，谢谢！')
        return self._code_branch

    @abc.abstractmethod
    def get_ocs_modelid(self):
        pass

    @abc.abstractmethod
    def get_ocs_require(self):
        pass