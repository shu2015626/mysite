# -*- coding: utf-8 -*-
'''
请写模块说明
'''
__author__ = "sunsn"
__date__ = '2018/9/1 15:49'

import random

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from login.models import EmailVerifyCode


def make_verify_code(str_length=16):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    verify_code = ''
    for i in range(str_length):
        verify_code += random.choice(chars)
    return verify_code


def send_verify_code(email, send_type='register'):
    obj_evc = EmailVerifyCode()
    if send_type == 'update_email':
        verify_code = make_verify_code(str_length=4).lower()
    else:
        verify_code = make_verify_code(str_length=16)

    obj_evc.code = verify_code
    obj_evc.email = email
    obj_evc.send_type = send_type
    obj_evc.save()

    if send_type == 'register':
        subject = '来自mysite的注册确认邮件'

        text_content = """
            感谢注册mysite，这里是我练习Django的地方
            如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！
        """
        html_content = '''
            <p>感谢注册<a href="http://{0}/active/{1}" target=blank>www.mysite.com</a>，\
            和我一起使用Django吧</p>
            <p>请点击站点链接完成注册确认！</p>
            <p>此链接在{2}小时内有效！</p>
        '''.format('127.0.0.1:8000', verify_code, settings.VARIFY_CODE_VALID_HOURS)

        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
        msg.attach_alternative(html_content, 'text/html')
        send_status = msg.send()
        if send_status:
            pass

    elif send_type == 'forget':
        pass
    elif send_type == 'update_email':
        pass

