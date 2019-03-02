# -*- coding: utf8 -*-
import  datetime

from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings

from .models import User, EmailVerifyCode
from .forms import UserForm, RegisterForm
from utils.encrypt import hash_code
from utils.email_oper import send_verify_code


class IndexView(View):
    def get(self, request):
        return render(request, 'login/index.html', {})


class LoginView(View):
    def get(self, request):
        if request.session.get('is_login', None):
            return redirect(to='/index/')

        login_form = UserForm()
        # return render(request, 'login/login.html', locals())
        return render(request, 'login/login.html', {'login_form': login_form})

    def post(self, request):
        login_form = UserForm(request.POST)
        message = "请检查填写的内容"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(nick_name=username)
                if not user.has_actived:
                    message = "该用户还未通过邮件确认！"
                    return render(request, 'login/login.html', {'message': message, 'login_form': login_form})
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.nick_name
                    return redirect(to='/index/')
                else:
                    # message = '密码不正确！'
                    message = "用户名或密码不正确"
            except Exception:
                    # message = '用户名不存在'
                    message = "用户名或密码不正确"
        # return render(request, 'login/login.html', locals())
        return render(request, 'login/login.html', {'message': message, 'login_form': login_form})

    # def post(self, request):
    #     username = request.POST.get('username', '')
    #     password = request.POST.get('password', '')
    #     if username and password:
    #         print(username, password)
    #         username = username.strip()
    #         try:
    #             user = User.objects.get(nick_name=username)
    #             if password == user.password:
    #                 return redirect('/index/')
    #             else:
    #                 # message = '密码不正确！'
    #                 message = "用户名或密码不正确"
    #         except Exception:
    #             # message = '用户名不存在'
    #             message = "用户名或密码不正确"
    #
    #         return render(request, 'login/login.html', {'message': message})
    #


class LogoutView(View):
    def get(self, request):
        if not request.session.get('is_login', None):
            return redirect('/index/')

        request.session.flush()
        # 或者使用下面的方法
        # del request.session['is_login']
        # del request.session['user_id']
        # del request.session['user_name']
        return redirect(to="/index/")


class RegisterView(View):
    def get(self, request):
        if request.session.get('is_login', None):
            return redirect("/index/")

        register_form = RegisterForm()
        return render(request, 'login/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = "两次输入的密码不同!"
                return render(request, 'login/register.html', {'register_form': register_form, 'message': message})
            else:
                same_name_user = User.objects.filter(nick_name=username)
                if same_name_user: # 用户名唯一
                    message = '用户名已经存在，请重新选择用户名'
                    return render(request, 'login/register.html', {'register_form': register_form, 'message': message})
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱'
                    return render(request, 'login/register.html', {'register_form': register_form, 'message': message})

            # 当一切都OK了
            new_user = User()
            new_user.nick_name = username
            new_user.password = hash_code(password1)
            new_user.email = email
            new_user.sex = sex
            new_user.save()

            send_verify_code(email, send_type='register')

            return redirect('/login/')
        else: # 数据验证失败
            return render(request, 'login/register.html', {'register_form': register_form, 'message': message})


class UserActiveView(View):
    def get(self, request, verify_code):
        try:
            verify_code_record = EmailVerifyCode.objects.get(code=verify_code)
        except Exception:
            message = '无效的确认请求'
            return render(request, 'login/active.html', {'message': message})

        create_time = verify_code_record.create_time
        now = datetime.datetime.now()
        user = User.objects.get(email=verify_code_record.email)
        if now > create_time + datetime.timedelta(hours=settings.VARIFY_CODE_VALID_HOURS):
            # 验证码过期，需要把用户删除
            user.delete()
            message = '您的邮件已经过期！请重新注册!'
            return render(request, 'login/active.html', {'message': message})
        else:
            user.has_actived = True
            user.save()
            verify_code_record.delete()
            message = '感谢确认，请使用账户登录！'
            return render(request, 'login/active.html', {'message': message})
