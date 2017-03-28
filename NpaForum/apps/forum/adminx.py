# _*_ coding:utf-8 _*_

import xadmin
from .models import *
from xadmin import views


class NodeAdmin(object):
    list_display = ['name', 'add_time']
    search_fields = ['name', 'add_time']
    list_filter = ['name', 'add_time']


class TopicAdmin(object):
    list_display = ['title', 'content', 'created_by', 'add_time', 'modify_time', 'click_nums', 'node']
    search_fields = ['title', 'content', 'created_by']
    list_filter = ['title', 'content', 'created_by']


class TabAdmin(object):
    list_display = ['name', 'add_time']
    search_fields = ['name', 'add_time']
    list_filter = ['name', 'add_time']

# 注册模型
xadmin.site.register(Node, NodeAdmin)
xadmin.site.register(Topic, TopicAdmin)
xadmin.site.register(Tab, TabAdmin)





