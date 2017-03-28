# _*_ coding:utf-8 _*_

"""NpaForum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from users.views import *
from operation.views import *
from forum.views import *
from settings import MEDIA_ROOT
from django.views.static import serve

import xadmin

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    # 注册
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # 登录
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    # 登出
    url(r'^logout/$', UserLogoutView.as_view(), name='logout'),
    # 忘记密码
    url(r'^forgot_pwd/$', ForgotPwdView.as_view(), name='forgot_pwd'),
    # 重设密码
    url(r'^reset_pwd/(?P<code>[a-zA-Z0-9]{1,32})/$', ResetPwdView.as_view(), name='reset_pwd'),

    # 创建主题
    url(r'^new/$', CreateTopicView.as_view(), name='create_topic'),
    # 主题详细
    url(r'^topic/(?P<topic_id>\d+)/$', TopicDetailView.as_view(), name='topic_detail'),
    # 回复主题
    url(r'^topic/reply/$', ReplyTopic.as_view(), name='topic_reply'),

    # 主页
    url(r'^$', IndexView.as_view(), name='index'),
    # 最近的主题
    url(r'^recent$', RecentTopicView.as_view(), name='recent_topic'),
    # 节点页面
    url(r'^node/(?P<node_id>\d+)$', NodeDetail.as_view(), name='node_detail'),
    # 添加收藏
    url(r'add_fav/$', AddFavorite.as_view(), name='add_fav'),
    # 搜索
    url(r'^search/$', SearchView.as_view(), name='search'),

    # 用户相关url
    url(r'^user/', include('users.urls', namespace='user')),

    # 媒体文件
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 验证码
    url(r'^captcha/', include('captcha.urls')),
]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
