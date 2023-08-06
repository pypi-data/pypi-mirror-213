import os
import sys

from lxml import etree
from openpyxl import Workbook
from openpyxl import load_workbook
from pyocs import pyocs_software
from pyocs.pyocs_analysis import PyocsAnalysis
from pyocs.pyocs_request import PyocsRequest
from pyocs.pyocs_demand import PyocsDemand
import My_pyocs_fun

# 创建对象
ocs_communication = My_pyocs_fun.child_pyocs()





#is_success = ocs_communication.upload_old_sw_by_id(ocs_num=ocs_number, old_sw_id=old_sw_id, burn_place_hold=burn_place_hold_type, burn_type=burn_type)
is_success = ocs_communication.reuse_old_sw_from_src_to_dst_by_fw_id('CP694722_JPE_VT0150UB1_0101_MT9602_PB823_SAUDI_ARABIA_V500DJ7_QE1_C8_4K_IR_VAPIR2A300_Logonai_PID20_7KEY_r223030_C_4K_PA_V0102.01.00T.L1125.zip','702754', os.getcwd())
#is_success = ocs_communication.reuse_old_sw_from_src_to_dst('579781','586477', os.getcwd())

