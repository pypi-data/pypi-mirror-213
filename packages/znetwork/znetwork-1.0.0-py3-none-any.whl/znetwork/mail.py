import smtplib
from email.mime.text import MIMEText


class Email:
    def __init__(self, server=None, port=None, user=None, password=None):
        self.server = server
        self.port = port
        self.user = user
        self.password = password

    def send(self, receiver, subject, content):
        message = MIMEText(content, 'plain', 'utf-8')
        message['Subject'] = subject  
        message['To'] = receiver
        message['From'] = self.user
        smtp = smtplib.SMTP_SSL(self.server, self.port)  
        smtp.login(self.user, self.password)  
        smtp.sendmail(self.user, [receiver], message.as_string())  
        smtp.close()
        print('发送邮件成功！！')

        