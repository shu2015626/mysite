# 教程代码实现
>教程：用户登录与注册系统  
>网址：http://www.liujiangblog.com/course/django/102

## 代码包含的内容(可以参考的内容, 后面写代码回头来抄~~)
### 1.代码的组织结构 
mysite: 项目名  
&emsp;&emsp;apps: 所以自己建立的app都放在该包下  
&emsp;&emsp;&emsp;&emsp;login:自己建立的app  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;templates：只适用本应用(app)的html模板  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;login：建一个和app同名的文件夹放html文件    
&emsp;&emsp;&emsp;&emsp;……  
&emsp;&emsp;&emsp;&emsp;utils:自己建立的app需要用到的公共的工具  
&emsp;&emsp;extra_apps：所有第三方的app都放在该包下  
&emsp;&emsp;&emsp;&emsp;captcha: 生成验证码的程序  
&emsp;&emsp;&emsp;&emsp;……  
&emsp;&emsp;media：所有用户上传的文件图片的存放目录（本项目没用到）   
&emsp;&emsp;mysite：和项目名同名的包，主配置文件  
&emsp;&emsp;statics: 存放前端静态资源  
&emsp;&emsp;&emsp;&emsp;bootstrap-3.3.7-dist   
&emsp;&emsp;&emsp;&emsp;css：前端的css资源  
&emsp;&emsp;&emsp;&emsp;font：前端的字体资源     
&emsp;&emsp;&emsp;&emsp;image：前端的图片资源  
&emsp;&emsp;&emsp;&emsp;js：前端的js资源  
&emsp;&emsp;templates:全局的html模板资源    
&emsp;&emsp;……其他的一些文件  
   
注：  
将应用移到apps和extra_apps中需要在settings.py中做一些事情
```python
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
```
### 2.FBV与CBV
django的视图有两种模式FBV(Function Base View)和CBV(Class Base View).  
教程是基于FBV做的视图，这部分代码使用的是CBV.不过提供了一个fbv的版本，便于学习  
注：本项目两种view使用的切换，只要修改mysite主配置包下的urls_cbv.py或者urls_fbv.py为urls.py即可


### 3.关于django的csrf（跨站请求伪造（英语：Cross-site request forgery））的防护  
（1）取消：
from django.views.decorators.csrf import csrf_exempt
并使用csrf_exempt装饰器修饰。如： 
```python
@csrf_exempt
def login(request):
    pass
``` 

（2）添加
在html页的form表单里添加{% csrf_token %}标签. 如：
```html
<form action="" method="post">
    {% csrf_token %}
    ....
</form>
```
具体请参见：apps/login/views_fbv.py

### 4.关于验证码（django-simple-captcha）
（1）需要先安装如下依赖的模块，具体的版本请酌情  
'six >=1.2.0'  
'Django >= 1.8'  
'Pillow >=2.2.2,!=5.1.0'  
'django-ranged-response == 0.2.0  
（2）关于使用：
请参见官方文档：https://django-simple-captcha.readthedocs.io/en/latest/usage.html
文档中的安装是：pip install  django-simple-captcha
不过我倾向于把源码放进来：extra_apps/captcha
（3）关于验证码点击刷新
```html
{% block custom_js %}
    <script>
        $('.captcha').click(function () {
            $.getJSON("/captcha/refresh/", function (result) {
                $('.captcha').attr('src', result['image_url']);
                $('#id_captcha_0').val(result['key'])
            });
        });
    </script>
{% endblock %}
```
参考：apps/login/templates/login/login.html或者apps/login/templates/login/register.html    
注意：模板中的{% block custom_js %}{% endblock %}一定要放到body元素的最后，因为顺序加载，需要其他的元素都有了才能起作用
### 5.其他
（1）安装app的两种方式
```python
INSTALLED_APPS = [
    ……
    'login.apps.LoginConfig',
    'captcha'
]
```
注：LoginConfig类在apps/login/apps.py文件中

(2)Form和ModelForm的生成。apps/login/forms.py  
里面各有一个例子。包括怎么向html标签传递class属性值等。  
详细请参考：http://www.liujiangblog.com/course/django/151
  
(3)使用reverse函数通过url的名字定位页面。如：  
```python
return redirect("/index/")
return redirect(reverse("index"))
```
这两个写法，第一个是直接将url地址写上，第二个则是通过url的名称，反解析出url地址。
为url地址赋给别名还有一个好处就是在html中也不用直接写url地址，
而是通过{% url 'url别名' 参数1 参数2 %}调用url,方便我们修改url地址  
请参考：apps/login/views_fbv.py


