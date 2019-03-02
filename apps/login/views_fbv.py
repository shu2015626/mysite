'''
视图：
django的视图有两种模式FBV(Function Base View)和CBV(Class Base View)

1.关于django的csrf_token的验证
1）取消：
from django.views.decorators.csrf import csrf_exempt
并使用csrf_exempt装饰器修饰
2）添加
在html页的form表单里添加{% csrf_token %}标签
'''
import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
from login import models
from login import forms
# from django.views import View
from utils.encrypt import hash_code
from utils.email_oper import send_verify_code

# Create your views here.

# 下面是FBV--function base view的写法

def index(request):
    return render(request, 'login/index.html')

# @csrf_exempt  # 不启用csrf防护
def login(request):
    if request.session.get('is_login', None):
        # return redirect("/index/")
        return redirect(reverse("index"))
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(nick_name=username)
                if not user.has_actived:
                    message = "该用户还未通过邮件确认！"
                    return render(request, 'login/login.html', {"message": message, 'login_form': login_form})
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.nick_name
                    # return redirect("/index/")
                    return redirect(reverse("index"))
                else:
                    message = "密码不正确！"
            except Exception:
                message = "用户不存在！"
        return render(request, 'login/login.html', {"message": message, 'login_form': login_form})

    login_form = forms.UserForm()
    return render(request, 'login/login.html', {'login_form': login_form})


def register(request):
    if request.session.get('is_login', None):
        # return redirect("/index/")
        return redirect(reverse('index'))
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码输入的是不是一样
                message = "两次输入的密码不同"
                return render(request, 'login/register.html', {'message': message, "register_form": register_form})
            else:
                same_name_user = models.User.objects.filter(nick_name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', {'message': message, "register_form": register_form})
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', {'message': message, "register_form": register_form})

                # 看起来数据符合我们的要求了，下面创建用户
                new_user = models.User()
                new_user.nick_name = username
                new_user.password = hash_code(password1)  # 或者password2
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                #发送激活验证码到邮箱
                send_verify_code(email)

                message = '请前往注册邮箱，进行邮件确认！'
                # return redirect("/login/", {"message": message})
                # return redirect(reverse("login"))  # 跳转到登录页面
                return render(request, 'login/active.html', {"message": message})  # 跳转到等待邮件确认页面。
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', {"register_form": register_form})


def logout(request):
    """注意比较这里的两个redirect，reverse是翻译url的name变成的url,拓展新更好"""
    if not request.session.get('is_login', None):
        # 如果本来就没登录，就没有登出的说法啦
        # return redirect("/index/")
        return redirect(reverse('index'))
    # 清空session数据
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']

    # return redirect("/index/")
    return redirect(reverse('index'))


def user_active(request, verify_code):
    try:
        obj_evc = models.EmailVerifyCode.objects.get(code=verify_code)
    except Exception:
        message = "无效的确认请求"
        return render(request, 'login/active.html', {"message": message})

    create_time = obj_evc.create_time
    now = datetime.datetime.now()
    user = models.User.objects.get(email=obj_evc.email)
    if now > create_time + datetime.timedelta(hours=settings.VARIFY_CODE_VALID_HOURS):
        user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/active.html', {"message": message})
    else:
        user.has_actived = True
        user.save()
        obj_evc.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/active.html', {"message": message})
