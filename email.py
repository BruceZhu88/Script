
import os
import time
import smtplib
import zipfile
# from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr


class UtilEmail(object):
    """
    """

    def __init__(self, info, context, type, attached=None):
        """
        info = {}
        type = plain or html
        attached = {}
        """

        self.info = info
        self.msg = MIMEMultipart()
        self.msg['From'] = self._format_addr(self.info['From'])
        self.msg['To'] = self._format_addr(self.info['To'])
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.msg['Subject'] = Header(
            self.info['Subject'], 'utf-8').encode() + " " + date
        self.msg.attach(MIMEText(context, type, 'utf-8'))
        self.process_attach(attached)
        self.password = self.info['Password']

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def process_attach(self, attached):

        if attached is None:
            return
        if len(attached) < 2:
            return
        if not os.path.exists(attached[0]):
            return
        file_name = 'result.zip'
        zippath = os.path.join(attached[0], file_name)
        azip = zipfile.ZipFile(file_name, 'w')
        for att in attached[1:]:
            path = os.path.join(attached[0], att)
            if os.path.isfile(path) and os.stat(path):
                azip.write(att, compress_type=zipfile.ZIP_DEFLATED)
        azip.close()
        # file_path = attached['filepath']
        # file_format = os.path.basename(file_path).rsplit('.')[1]
        # file_name = os.path.basename(file_path)
        # file_type = attached['type']
        att1 = MIMEText(
            open(zippath, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="%s"' % file_name
        self.msg.attach(att1)

    def send(self):
        server = smtplib.SMTP(self.info['smtp_server'], 25)
        server.set_debuglevel(1)
        from_addr = parseaddr(self.info['From'])[1]
        to_addr = parseaddr(self.info['To'])[1]
        server.login(from_addr, self.password)
        server.sendmail(from_addr, [to_addr], self.msg.as_string())
        server.quit()


if __name__ == '__main__':
    email_info = {
        'smtp_server': 'smtp.163.com',
        'Password': '459643556',
        'From': 'Bruce <a76748328@163.com>',
        'To': '管理员 <459643556@qq.com>',
        'Subject': '来自SMTP的问候……'
    }
    context = """
<html>
<body>
<h1>Hello</h1>
<p>send by <a href="http://www.python.org">Python</a>...</p>
</body>
</html>
"""
    attached = ['C:/Users/zhujialin/Desktop/', 'test.txt', 'bg.jpg']

    util_email = UtilEmail(email_info, context, 'html', attached=attached)
    util_email.send()
