# _*_ coding:utf-8 _*_

from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from NpaForum.settings import *


def send_func_mail(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.send_type = send_type
    email_record.email = email
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'forget':
        email_title = '重置密码'
        email_body = '点此链接重置：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


def random_str(srt_length=8):
    _str = ''
    char = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890'
    random = Random()
    char_length = len(char) - 1
    for i in range(srt_length):
        _str += char[random.randint(0, char_length)]
    return _str

