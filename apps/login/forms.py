# -*- coding: utf-8 -*-
'''
请写模块说明
'''
__author__ = "sunsn"
__date__ = '2018/9/1 12:20'

from django import forms
from .models import User
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['nick_name', 'password']
#
#     def __init__(self, *args, **kwargs):
#         # super(UserForm, self).__init__(*args, **kwargs)
#         super().__init__(self, *args, **kwargs)
#         self.fields['nick_name'].label = '用户名'
#         self.fields['password'].label = '密码'


class RegisterForm(forms.Form):
    GENDER = (
        ('male', '男'),
        ('female', '女')
    )

    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='邮箱地址', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=GENDER)
    captcha = CaptchaField(label='验证码', error_messages={"invalid": "验证码错误"})

