# _*_ coding:utf-8 _*_

from django.conf.urls import url
from .views import *

urlpatterns = [
    # 用户中心
    url(r'^(?P<user_id>\d+)/$', UserCenterView.as_view(), name='user_center'),
    # 用户收藏
    url(r'^fav/(?P<fav_type>[a-z]+)/$', UserFavoriteView.as_view(), name='user_fav'),
    # 设置中心
    url(r'^setting/$', UserSettingView.as_view(), name='user_setting'),
    # 头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='user_image_upload'),
    # 修改密码
    url(r'^modify_pwd/$', UpdatePwdView.as_view(), name='user_modify_pwd'),
]

