# -*- coding: utf8 -*-

from __future__ import unicode_literals
from users.models import *
from datetime import datetime

from django.db import models

# Create your models here.


class UserFavorite(models.Model):
    """用户收藏模型"""
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField(default=0, verbose_name='数据id')
    fav_type = models.CharField(choices=(('topic', 'topic'), ('node', 'node'), ('user', 'user')), max_length=10,
                                verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')


