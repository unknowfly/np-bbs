# -*- coding: utf8 -*-

from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from users.models import UserProfile

# Create your models here.


class Tab(models.Model):
    name = models.CharField(max_length=50, verbose_name='标签名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def getNodes(self):
        return Node.objects.filter(tab=self)

    def __unicode__(self):
        return self.name


class Node(models.Model):
    name = models.CharField(max_length=50, verbose_name='节点名称', unique=True)
    tab = models.ForeignKey(Tab, verbose_name='所属标签', null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    desc = models.CharField(default='', max_length=200, verbose_name='描述')
    image = models.ImageField(max_length=200, upload_to='image/%Y/%m', null=True, default='image/default/node.png',
                              verbose_name='节点图片')

    class Meta:
        verbose_name = '论坛节点'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    node = models.ForeignKey(Node, verbose_name='节点', null=True)
    created_by = models.ForeignKey(UserProfile, verbose_name='创建者')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    modify_time = models.DateTimeField(verbose_name='修改时间', blank=True, null=True)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    # last_reply_user = models.CharField(max_length=50, verbose_name='最新回复用户名', null=True, default='')

    class Meta:
        verbose_name = '主题'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class Reply(models.Model):
    content = models.TextField(verbose_name='内容')
    created_by = models.ForeignKey(UserProfile, verbose_name='创建者')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    modify_time = models.DateTimeField(verbose_name='修改时间', blank=True, null=True)
    topic = models.ForeignKey(Topic, verbose_name='所属主题')
    seq_num = models.IntegerField(verbose_name='序号')

    class Meta:
        verbose_name = '主题回复'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.topic.title[:20] + str(self.seq_num) + 'L 回复'

