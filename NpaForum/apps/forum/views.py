# _*_ coding:utf-8 _*_

from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from markdown2 import markdown
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from utils.common_utils import *
from operation.models import *
from utils.data_utils import *

# Create your views here.


class TopicDetailView(View):
    def get(self, request, topic_id):
        print datetime.now()
        if int(topic_id) > 0:
            topic = Topic.objects.get(pk=int(topic_id))
            if topic:
                topic.click_nums += 1
                topic.save()
                topic.time_span = time_span(topic.add_time)
                last_reply = topic.reply_set.order_by('-add_time')[:1]
                if last_reply:
                    topic.last_reply_time = time_span(last_reply[0].add_time)
                reply_list = topic.reply_set.all()

                try:
                    page = request.GET.get('page', 1)
                except PageNotAnInteger:
                    page = 1

                p = Paginator(reply_list, 10, request=request)

                reply_list = p.page(page)

                has_fav_topic = False
                if request.user.is_authenticated():
                    if UserFavorite.objects.filter(user=request.user, fav_type='topic', fav_id=topic.id):
                        has_fav_topic = True
                topic.fav_nums = UserFavorite.objects.filter(fav_type='topic', fav_id=topic.id).count()

                context = get_context()
                context['topic'] = topic
                context['reply_list'] = reply_list
                context['has_fav_topic'] = has_fav_topic

                return render(request, 'topic-detail.html', context)
            else:
                pass
        else:
            pass


class IndexView(View):
    """主页视图"""
    def get(self, request):
        current_tab = request.GET.get('tab')
        if not current_tab:
            current_tab = 1
        else:
            current_tab = int(current_tab)
        tab_node_list = Tab.objects.get(pk=current_tab).getNodes()
        topic_list = Topic.objects.filter(node__in=[x.id for x in tab_node_list]).order_by('-add_time')[0:15]

        for i in topic_list:
            i.time_span = time_span(i.add_time)
            i.last_reply = i.reply_set.order_by('-add_time')[:1]

        context = get_context()
        context['topic_list'] = topic_list
        context['current_tab'] = current_tab
        context['tab_node_list'] = tab_node_list

        return render(request, 'index.html', context)


class RecentTopicView(View):
    """最近所有主题视图"""
    def get(self, request):
        topic_list = Topic.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(topic_list, 10, request=request)

        topic_list = p.page(page)

        for i in topic_list.object_list:
            i.time_span = time_span(i.add_time)
            i.last_reply = i.reply_set.order_by('-add_time')[:1]

        context = get_context()
        context['topic_list'] = topic_list

        return render(request, 'recent-topic.html', context)


class NodeDetail(View):
    """节点主页视图"""
    def get(self, request, node_id):
        node = Node.objects.get(pk=node_id)
        topic_list = Topic.objects.filter(node_id=node_id).order_by('-add_time')
        topic_count = topic_list.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(topic_list, 10, request=request)

        topic_list = p.page(page)

        for i in topic_list.object_list:
            i.time_span = time_span(i.add_time)
            i.last_reply = i.reply_set.order_by('-add_time')[:1]

        has_fav_node = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type='node', fav_id=node.id):
                has_fav_node = True

        context = get_context()
        context['node'] = node
        context['topic_list'] = topic_list
        context['has_fav_node'] = has_fav_node
        context['topic_count'] = topic_count

        return render(request, 'node-home.html', context)


class SearchView(View):
    """站内搜索视图"""
    def post(self, request):
        keyword = request.POST.get('keyword')
        topic_list = Topic.objects.filter(Q(content__icontains=keyword) | Q(title__icontains=keyword)).order_by('-add_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(topic_list, 10, request=request)

        topic_list = p.page(page)

        for i in topic_list.object_list:
            i.time_span = time_span(i.add_time)
            i.last_reply = i.reply_set.order_by('-add_time')[:1]

        context = get_context()
        context['keyword'] = keyword
        context['topic_list'] = topic_list

        return render(request, 'search-result.html', context)

