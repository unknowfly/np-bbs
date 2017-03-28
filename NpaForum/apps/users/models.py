# -*- coding: utf8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

from utils.common_utils import *
# Create your models here.


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=60, verbose_name='昵称')
    birthday = models.DateField(blank=True, null=True, verbose_name='生日')
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), max_length=10, verbose_name='性别')
    address = models.CharField(max_length=200, verbose_name='地址')
    mobile = models.CharField(max_length=20, verbose_name='移动电话', blank=True, null=True)
    image = models.ImageField(max_length=200, upload_to='image/%Y/%m', default='image/default/avatar.png', verbose_name='头像')
    website = models.CharField(max_length=50, verbose_name='个人网站', blank=True, default='')
    fav_topic_nums = models.IntegerField(default=0, verbose_name='收藏主题数')
    fav_node_nums = models.IntegerField(default=0, verbose_name='收藏节点数')
    fav_user_nums = models.IntegerField(default=0, verbose_name='收藏用户数')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=50, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(choices=(('用户注册', 'register'), ('忘记密码', 'forgot_pwd'),
                                          ('更改注册邮箱', 'update_email')), verbose_name='验证码类型', max_length=50)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.send_type + self.email




