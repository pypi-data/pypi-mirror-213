@echo off
Set ws = CreateObject("Wscript.Shell")
wscript.sleep 1200 ws.run "cmd /c start C:\Users\cvte\Desktop\pyocs-master\pyocs-master\customers\customer_jinpin\test_success_confirm\auto_get_excel.bat",vbhide

cd C:\Users\cvte\Desktop\pyocs-master\pyocs-master

python customers/customer_jinpin/test_success_confirm/CheckCustomerConfirmExcelEmail.py

exit