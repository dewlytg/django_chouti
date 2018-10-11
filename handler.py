import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback
import random


class BaseResponse:
    def __init__(self):
        self.status = True
        self.summary = None
        self.errors = {}
        self.data = None


def generator_verification_code():
    character = []
    # 所有大写字母
    for i in range(65, 91):
        character.append(chr(i))
    # 所有小写字母
    for i in range(97, 123):
        character.append(chr(i))
    # 所有数字
    for i in range(48, 58):
        character.append(chr(i))
    return "".join(random.sample(character, 4))


def send_mail(to_addr,body,subject="抽屉验证码"):
    try:
        from_addr = "zabbix@cutt.com"
        password = "Hello1234"
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP("smtp.mxhichina.com")
        server.starttls()
        server.login(from_addr, password)
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
    except smtplib.SMTPException:
        traceback.print_exc()
    finally:
        server.quit()

