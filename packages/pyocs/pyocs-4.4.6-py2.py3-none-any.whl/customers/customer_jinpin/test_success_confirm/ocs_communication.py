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
is_success = ocs_communication.reuse_old_sw_from_src_to_dst_by_fw_id('CS676902_JPE_SK708D_PC821_ISRAEL_V500DJ7_QE1_C3_01202108074_E50DM1100_8G_1G_P_7KEY_REF59_V3_4_0_TWO_DIV_3af452f2_20210908_104145.zip','675693', os.getcwd())
#is_success = ocs_communication.reuse_old_sw_from_src_to_dst('579781','586477', os.getcwd())

