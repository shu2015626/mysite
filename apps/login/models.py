from django.db import models

# Create your models here.


class User(models.Model):
    GENDER = (
        ('male', '男'),
        ('female', '女')
    )

    nick_name = models.CharField(max_length=128, unique=True, verbose_name='昵称')
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    sex = models.CharField(max_length=32, choices=GENDER, default='male', verbose_name='性别')
    has_actived = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='记录添加时间')

    class Meta:
        ordering = ['-create_time']
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nick_name


class EmailVerifyCode(models.Model):
    VERIFY_CODE_TYPE = (
        ('register', "注册"),
        ('forget', '找回密码'),
        ('update_email', '修改邮箱')
    )
    code = models.CharField(max_length=256)
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(verbose_name="验证码类型", choices=VERIFY_CODE_TYPE, max_length=15)
    create_time = models.DateTimeField(verbose_name="发送时间", auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)

