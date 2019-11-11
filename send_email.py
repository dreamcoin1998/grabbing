import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os


class MyEmail:
    def __init__(self, tag='页面已更新', html='res.html'):
        self.user = 'gaojunbin@gaoblog.cn'
        self.passwd = 'xfYC4mkT2QLPuBQv'
        self.to_list = ['1285338586@qq.com']
        self.cc_list = ['1285338586@qq.com']
        self.tag = tag
        self.html = html

    def send(self):
        """
        发送邮件
        """
        try:
            server = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)
            server.login(self.user, self.passwd)
            server.sendmail("<%s>" % self.user, self.to_list, self.get_attach())
            server.close()
            print("send email successful")
        except Exception as e:
            print("send email failed %s" % e)

    def get_attach(self):
        """
        构造邮件内容
        """
        attach = MIMEMultipart()
        if self.tag is not None:
            # 主题,最上面的一行
            attach["Subject"] = self.tag
        if self.user is not None:
            # 显示在发件人
            attach["From"] = "<%s>" % self.user
        if self.to_list:
            # 收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            # 抄送列表
            attach["Cc"] = ";".join(self.cc_list)
        if self.html:
            # 估计任何文件都可以用base64，比如rar等
            # 文件名汉字用gbk编码代替
            name = os.path.basename(self.html).encode("utf8")
            f = open(self.html, "rb")
            html = MIMEText(f.read(), "html", "utf-8")
            attach.attach(html)
            f.close()
        return attach.as_string()