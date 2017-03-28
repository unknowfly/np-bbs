# _*_ coding:utf-8 _*_

from forum.models import *
from users.models import UserProfile


def get_context():
    context = {}
    tab_list = Tab.objects.all()

    context['tab_list'] = tab_list
    context['forum_user_count'] = UserProfile.objects.count()
    context['forum_topic_count'] = Topic.objects.count()

    return context


