# _*_ coding:utf-8 _*_

import xadmin
from .models import *
from xadmin.plugins.auth import UserAdmin
from xadmin import views


class GlobalSetting(object):
    """
    后台面板基础配置信息
    """
    site_title = '社区后台管理'
    site_footer = 'npa-bbs'
    menu_style = 'accordion'


class UserProfileAdmin(UserAdmin):
    pass


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type']
    model_icon = 'fa fa-user'


# 注册模型
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.CommAdminView, GlobalSetting)








