import poplib
import time
import telnetlib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import re
class mail_tool:
    _instance = None

    # 单例模式
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(mail_tool, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        pass

    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode("gbk")
        return value

    def guess_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset



    def get_mail_text(self, msg, indent=0):
        # indent用于缩进显示
        text = ''
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header=='Subject':
                        value = self.decode_str(value)
                    else:
                        hdr, addr = parseaddr(value)
                        name = self.decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                text += '%s%s: %s\n' % ('  ' * indent, header, value)
        if (msg.is_multipart()):
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                text += self.get_mail_text(part, indent + 1)
        else:
            content_type = msg.get_content_type()
            if content_type == 'text/plain':
                content = msg.get_payload(decode=True)
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode("gbk")
                text += '%sText: %s' % ('  ' * indent, content)
        return text

    def get_base_sw_name_and_config_name(self, text):
        #for jinpin , get the base sw name and config name from mail
        regular = re.compile(r'\d{8}_\d{6}')
        base_name = re.findall(regular, text)[0][0:15]
        if len(base_name) > 1:
            return [base_name, base_name[1]]
        else:
            return [base_name, '']

    def get_oder_num_and_board(self, text):
        #金品专用，拿到评审单号，主板型号
        regular = re.compile(r'TWBZ[\w|-]*\.\w*\.')
        tmp = re.findall(regular, text)[0]
        return [tmp[17:30], tmp[33:38]]

if __name__ == "__main__":

    email = 'linxiangna@cvte.com'
    passwd = 'Lin13690439782?'
    pop3_server = "pop.cvte.com"


    sys_time = time.strftime('time:%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    print(sys_time)
    telnetlib.Telnet('pop.cvte.com', 995)
    server = poplib.POP3_SSL(pop3_server, 995, timeout=10)

    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))

    server.user(email)
    server.pass_(passwd)

    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    # print(mails)

    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)
    resp, lines, octets = server.retr(index)

    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)

    text = mail_tool().get_mail_text(msg)
    print(text)
    print(mail_tool().get_base_sw_name_and_config_name(text))
    print(mail_tool().get_oder_num_and_board(text))
    # 可以根据邮件索引号直接从服务器删除邮件:
    # server.dele(index)
    # 关闭连接:
    server.quit()
    '''
    text = "DZ.20210729-001耶鲁尔TWBZ-01-2106-019201-202106-199TP.SK108.PB818_V53E32DM1100PT320AT03-3(HD)廖小平"
    regular2 = re.compile(r'TWBZ.*\.\w*\.')
    config_name = re.findall(regular2, text)
    print(config_name)
    '''