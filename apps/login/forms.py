# -*- coding: utf-8 -*-
'''
请写模块说明
'''
__author__ = "sunsn"
__date__ = '2018/9/1 12:20'

from django import forms
from login import models
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.ModelForm):
    """为了学习ModelForm,使用模型生成一部分字段(email, sex)"""
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label="验证码", error_messages={'invalid': "验证码错误"})

    class Meta:
        model = models.User
        fields = ['email', 'sex']
        labels = {
            # "sex": _('sex'),  # 会翻译, 但没翻译
            "sex": "性别",
            "email": "邮箱地址"
        }
        widgets = {
            # 如果模型字段设置了choices参数，那么表单字段的widget属性将设置成Select框，其选项来自模型字段的choices。
            # sex在User模型中是choices选择的，会自动搞定的，如果这里做的话，可以这样写
            # "sex": forms.Select(choices=models.User.GENDER_CHOICES)  # 有限懒不想在定义这个选项
            "email": forms.EmailInput(attrs={"class": "form-control"})
        }


# class RegisterForm(forms.Form):
#     """纯手工生成form"""
#     GENDER = (
#         ('male', '男'),
#         ('female', '女')
#     )
#
#     username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(label='邮箱地址', widget=forms.EmailInput(attrs={'class': 'form-control'}))
#     sex = forms.ChoiceField(label='性别', choices=GENDER)
#     captcha = CaptchaField(label='验证码', error_messages={"invalid": "验证码错误"})

