from django.contrib import admin
from mainapp.models import MyUser, UsersInfo
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.register(UsersInfo)


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'mobile', 'qq', 'wechat']

    # 在用户信息修改界面添加'mobile','qq','wechat'的信息输入框
    # 将源码的UserAdmin.fieldsets转换成列表格式
    fieldsets = list(UserAdmin.fieldsets)
    # 重写UserAdmin的fieldsets, 添加'mobile'、'qq'、'wechat'的信息录入
    fieldsets[1] = (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'mobile', 'qq', 'wechat')})

