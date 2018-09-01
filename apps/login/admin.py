from django.contrib import admin

# Register your models here.

from .models import User, EmailVerifyCode


class UserAdmin(admin.ModelAdmin):
    list_display = ['nick_name', 'password', 'email', 'sex', 'create_time']
    search_fields = ['nick_name', 'email']
    list_filter = ['nick_name', 'email', 'sex', 'create_time']


class EmailVerifyCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'email', 'send_type', 'create_time']
    search_fields = ['email', 'send_type']
    list_filter = ['email', 'send_type', 'create_time']


admin.site.register(User, UserAdmin)
admin.site.register(EmailVerifyCode, EmailVerifyCodeAdmin)

