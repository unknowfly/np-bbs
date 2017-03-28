# _*_ coding:utf-8 _*_

import json

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from markdown2 import markdown

from utils.mixin_utils import *
from .models import *
from forum.models import *
from utils.data_utils import *
# Create your views here.


class CreateTopicView(LoginRequiredMixin, View):
    """创建主题视图"""
    def get(self, request):
        node_list = Node.objects.all()

        context = get_context()
        context['node_list'] = node_list

        return render(request, 'create-topic.html', context)

    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        node_id = request.POST.get('node')
        topic = Topic(title=title, content=markdown(content), created_by=request.user, node_id=int(node_id))
        topic.save()
        res = {'success': True, 'topic_id': topic.id}
        return HttpResponse(json.dumps(res), content_type='application/json')


class ReplyTopic(LoginRequiredMixin, View):
    """发表回复视图"""
    def post(self, request):
        topic_id = request.POST.get('topic_id')
        content = request.POST.get('content')
        if int(topic_id) > 0:
            reply = Reply(topic_id=int(topic_id), content=markdown(content), created_by=request.user)
            reply.seq_num = Reply.objects.filter(topic_id=int(topic_id)).all().count() + 1
            reply.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'success': False}), content_type='application/json')


class AddFavorite(View):
    def post(self, request):
        fav_type = request.POST.get('fav_type')
        data_id = request.POST.get('data_id')
        user_fav = UserFavorite()
        text = ''

        exist_record = UserFavorite.objects.filter(user=request.user, fav_type=fav_type, fav_id=int(data_id))
        if exist_record:
            exist_record.delete()
            user_fav_nums_opt(fav_type, request.user, 'minus')
            if fav_type == 'user':
                text = '关注此人'
            else:
                text = '加入收藏'
            return HttpResponse(json.dumps({'success': True, 'text': text}), content_type='application/json')
        else:
            user_fav.user = request.user
            user_fav.fav_type = fav_type
            user_fav.fav_id = data_id
            user_fav.save()
            user_fav_nums_opt(fav_type, request.user, 'plus')
            if fav_type == 'user':
                text = '取消关注'
            else:
                text = '取消收藏'
            return HttpResponse(json.dumps({'success': True, 'text': text}), content_type='application/json')

