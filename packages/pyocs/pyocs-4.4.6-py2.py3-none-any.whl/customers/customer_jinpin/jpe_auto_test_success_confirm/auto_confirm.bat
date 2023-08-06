@echo off
Set ws = CreateObject("Wscript.Shell")
wscript.sleep 1200 ws.run "cmd /c start C:\Users\cvte\Desktop\pyocs-master\pyocs-master\customers\customer_jinpin\test_success_confirm\auto_confirm.bat",vbhide

cd C:\Users\cvte\Desktop\pyocs-master\pyocs-master

python customers/customer_jinpin/test_success_confirm/jinpin_auto_confirm_software_by_email.py

exit