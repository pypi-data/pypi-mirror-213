import datetime
import email
import poplib
import email.policy
import telnetlib
import time
import os
import json
import sys
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from pyocs import pyocs_login
import global_var as gl    #添加全局变量管理模块
pop3_server = 'pop.cvte.com'
poplib._MAXLINE=20480
#=============================================================
# 脚本介绍和说明：
# 1、在CVTE企业网页邮箱里设置把收取3个月的邮件改成收取全部
# 2、这个脚本第一次运行会生产一个文件counttxt.txt记录目前邮件数
# 3、下次运行会获取最新的邮件的数，然后处理新增的邮件
#==============================================================
gl._init()
class CheckCustomerConfirmExcelEmail:

    subject_title="订单软件确认"
    account = pyocs_login.PyocsLogin().get_account_from_json_file()
    from_addr = str(account['Username']) + "@cvte.com"
    password = account['Password']

    email_user = 'linxiangna@cvte.com'
    dirPath = os.getcwd()

    #记录邮件个数文件的路径
    counttxtpath= dirPath+'/customers/customer_jinpin/test_success_confirm/counteConfirmEmail.xlsx'
    AttachName = "回复CVT软件信息"#"软件确认汇总"
    # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
    confirmfilepath=dirPath+'/customers/customer_jinpin/test_success_confirm/confirm_excel/'
    save_confirm_file_name=dirPath+'/customers/customer_jinpin/test_success_confirm/confirm_file_name.txt'
    

    # 解析邮件,获取附件
    def get_att(self,msg_in):
        # import email
        attachment_files = []
        for part in msg_in.walk():
            # 获取附件名称类型
            file_name = part.get_filename()
            if file_name:
                h = email.header.Header(file_name)
                # 对附件名称进行解码
                dh = email.header.decode_header(h)
                filename = dh[0][0]
                if dh[0][1]:
                    # 将附件名称可读化
                    filename = self.decode_str(str(filename, dh[0][1]))
                    print("附件名:"+str(filename))
                    if self.AttachName in str(filename):  
                        # filename = filename.encode("utf-8")
                        # 下载附件
                        data = part.get_payload(decode=True)
                        print(filename)
                        att_file = open(self.confirmfilepath+filename, 'wb')
                        attachment_files.append(filename)
                        att_file.write(data)  # 保存附件
                        att_file.close()
                        fw = open(self.save_confirm_file_name, 'w',encoding='utf-8',errors='ignore')
                        fw.write(str(filename))
                        fw.close() 
                        #global recive_new_email_flag
                        gl.set_recive_new_email_flag(True)
                        print("recive",gl.get_recive_new_email_flag())                  
                        print("找到了，退出！")
                        exit()
        return attachment_files

    #==============================================================
    # 解析邮件必要的一些字符转换
    #==============================================================
    def decode_str(self,s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value
class Logger(object):
    def __init__(self, filename='getexcel.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
#global recive_new_email_flag    
#Check_in_confirm = CheckCustomerConfirmExcelEmail.CheckCustomerConfirmExcelEmail()
#CheckCustomerConfirmExcelEmail Check_in_confirm = Che



#==============================================================
# 主程序
# 登录邮箱。获取邮件个数，对比处理新增邮件个数
# 将名称含有subject_title 特殊字符的邮件才进行解析处理。
#==============================================================
if __name__ == '__main__':
    # 连接到POP3服务器,有些邮箱服务器需要ssl加密，可以使用poplib.POP3_SSL
    try:
  
        sys.stdout = Logger(stream=sys.stdout)
        sys.stdout = Logger(stream=sys.stderr)
        sys_time=time.strftime('time:%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        print(sys_time)  
        telnetlib.Telnet('pop.cvte.com', 995)
        server = poplib.POP3_SSL(pop3_server, 995, timeout=10)
    except:
        time.sleep(5)
        server = poplib.POP3(pop3_server, 110, timeout=10)

    # 可以打开或关闭调试信息
    # server.set_debuglevel(1)
    # 打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))
    Che = CheckCustomerConfirmExcelEmail()
    # 身份认证:
    server.user(Che.email_user)
    server.pass_(Che.password)
    # 返回邮件数量和占用空间
    print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    new_email_num = len(mails)
    print("当前邮件个数 ="+str(new_email_num))

    if os.path.exists(Che.counttxtpath):
        #记录文件存在
        fr =open(Che.counttxtpath)
        old_email_num = fr.read()

        if (str(old_email_num) == str(new_email_num)):
            #没有新邮件
            print("没有新邮件")
            fr.close()
        else:
            #有新邮件，得到邮件个数差值
            dif_value = int(new_email_num) - int(old_email_num)
            fr.close()
            #记录新的邮件个数
            fw = open(Che.counttxtpath, 'w',encoding='utf-8',errors='ignore')
            fw.write(str(new_email_num))
            fw.close()

            #print(int(old_email_num))
            #print(int(new_email_num))
            for index in range(int(old_email_num)+1, int(new_email_num)+1):
                resp, lines, octets = server.retr(index)
                # lines存储了邮件的原始文本的每一行
                # 邮件的原始文本:
                msg_content = b'\r\n'.join(lines).decode('utf-8','ignore')
                msg = Parser().parsestr(msg_content)
                Che.get_att(msg)
                print("\n\n-------------------------------一封邮件处理完毕-------------------------------\n\n")
                #subject_str = decode_str(msg.get('Subject',''))
                #if subject_title in str(subject_str):
                #    print(subject_str)
                #    get_email_txt(msg)
                #    print("\n\n-------------------------------一封邮件处理完毕-------------------------------\n\n")
            #关闭连接
            server.quit()
    else:
        #记录文件不存在
        #第一次运行,创建并写入文件
        f = open(Che.counttxtpath, 'w',encoding='utf-8',errors='ignore')
        f.write(str(new_email_num))
        f.close()
