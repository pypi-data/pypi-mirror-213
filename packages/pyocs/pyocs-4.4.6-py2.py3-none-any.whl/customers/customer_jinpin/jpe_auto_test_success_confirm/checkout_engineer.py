from openpyxl import load_workbook

import logging


class get_engineer:
   _logger = logging.getLogger(__name__)

   def __init__(self):
      self._logger.setLevel(level=logging.WARNING)  # 控制打印级别
   # #映射字典或者集合或者数组（工程师对方案，一对多）
   #获取方案的函数
   #通过输入的方案，返回工程师（空的情况）

   en_chenchaoxiong=["516","69","6710","5507","358","5522","508","553","3458"]
   en_linxiangna=["59","3553","512","638","338","5510","960","320","ATM30","708","972","530","3683","702"]
   en_hejian=["706"]
   en_chenjiayi8469=["3663","69","56","108","53","9632","506","U63","706","518"]

		
		
   #做法二
   #fangan为直接获取的单元格数值
   #fangan="TP.HV553.PC821"

   def check_engineer_name(slef,fangan):
      for str_fangan in slef.en_linxiangna:
         if str_fangan in fangan:
             ret="linxiangna@cvte.com"
             return ret

      for str_fangan in slef.en_hejian:
         if str_fangan in fangan:
             ret="hejian@cvte.com"
             return ret

      for str_fangan in slef.en_chenchaoxiong:
         if str_fangan in fangan:
             ret="chenchaoxiong@cvte.com"
             return ret

      for str_fangan in slef.en_chenjiayi8469:
         if str_fangan in fangan:
             ret="chenjiayi8469@cvte.com"
             return ret
      ret="linxiangna@cvte.com"
      return ret



