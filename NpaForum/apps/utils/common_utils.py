# _*_ coding:utf-8 _*_

from datetime import datetime


def time_span(ts):
    """计算时间差"""
    delta = datetime.now() - ts.replace(tzinfo=None)

    if delta.days >= 365:
        return '%d年前' % (delta.days / 365)
    elif delta.days >= 30:
        return '%d个月前' % (delta.days / 30)
    elif delta.days > 0:
        return '%d天前' % delta.days
    elif delta.seconds < 60:
        return "%d秒前" % delta.seconds
    elif delta.seconds < 60 * 60:
        return "%d分钟前" % (delta.seconds / 60)
    else:
        return "%d小时前" % (delta.seconds / 60 / 60)


def user_fav_nums_opt(fav_type, user, opt):
    if fav_type == 'topic':
        if opt == 'plus':
            user.fav_topic_nums += 1
        else:
            user.fav_topic_nums -= 1
    elif fav_type == 'node':
        if opt == 'plus':
            user.fav_node_nums += 1
        else:
            user.fav_node_nums -= 1
    elif fav_type == 'user':
        if opt == 'plus':
            user.fav_user_nums += 1
        else:
            user.fav_user_nums -= 1
    user.save()





