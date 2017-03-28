# _*_ coding:utf-8 _*_
from datetime import timedelta
import json

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import *
from forum.models import *
from utils.common_utils import *
from operation.models import *
from utils.mixin_utils import *
from utils.data_utils import *
from utils.email_utils import *
# Create your views here.


class CustomBackend(ModelBackend):
    """
    自定义登陆
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None


class RegisterView(View):
    """
    用户注册视图
    """
    def get(self, request):

        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))

        user = UserProfile()
        register_form = RegisterForm(instance=user)

        context = get_context()
        context['register_form'] = register_form

        return render(request, 'register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)

        context = get_context()

        if register_form.is_valid():
            user_inst = register_form.save(commit=False)
            user_inst.password = make_password(user_inst.password)
            user_inst.save()
            context['register_success'] = True
            return render(request, 'register.html', context)
        else:
            context['register_form'] = register_form
            return render(request, 'register.html', context)


class UserLoginView(View):
    """
    用户登录视图
    """
    def get(self, request):

        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))

        return render(request, 'login.html', get_context())

    def post(self, request):
        login_form = LoginForm(request.POST)

        context = get_context()

        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                context['register_form'] = login_form
                context['msg'] = '用户名或密码错误'
                return render(request, 'login.html', context)
        else:
            context['register_form'] = login_form
            context['msg'] = '用户名或密码错误'
            return render(request, 'login.html', context)


class UserLogoutView(View):
    """用户登出"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class ForgotPwdView(View):
    """忘记密码"""
    def get(self, request):
        forgot_pwd_form = ForgotPwdForm()
        context = get_context()
        context['forgot_pwd_form'] = forgot_pwd_form
        return render(request, 'find_pwd.html', context)

    def post(self, request):
        forgot_pwd_form = ForgotPwdForm(request.POST)
        context = get_context()

        if forgot_pwd_form.is_valid():
            email = request.POST.get('email', '')
            send_func_mail(email, 'forget')
            context['send_success'] = True
            return render(request, 'find_pwd.html', context)
        else:
            context['forgot_pwd_form'] = forgot_pwd_form
            return render(request, 'find_pwd.html', context)


class ResetPwdView(View):
    """重置密码视图"""
    def get(self, request, code):
        email_verify = EmailVerifyRecord.objects.get(code=code)
        if email_verify:
            context = get_context()
            context['code'] = code
            return render(request, 'reset_pwd.html', context)
        else:
            return render(request, '404.html', {})

    def post(self, request, code):
        _code = request.POST.get('reset_code')
        email_verify = EmailVerifyRecord.objects.get(code=_code)
        if email_verify:
            context = get_context()
            reset_pwd_form = ResetPwdForm(request.POST)
            if reset_pwd_form.is_valid():
                user = UserProfile.objects.get(email=email_verify.email)
                user.password = make_password(password=reset_pwd_form.cleaned_data.get('password'))
                user.save()
                email_verify.delete()

                context['reset_success'] = True
                return render(request, 'reset_pwd.html', context)
            else:
                context['code'] = _code
                context['reset_success'] = False
                context['reset_pwd_form'] = reset_pwd_form
                return render(request, 'reset_pwd.html', context)
        else:
            return render(request, '404.html', {})


class UserCenterView(View):
    """用户中心视图"""
    def get(self, request, user_id):
        user = UserProfile.objects.get(id=int(user_id))
        topic_list = user.topic_set.all().order_by('-add_time')

        has_fav_user = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type='user', fav_id=user.id):
                has_fav_user = True

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(topic_list, 10, request=request)

        topic_list = p.page(page)

        if topic_list:
            for i in topic_list.object_list:
                i.time_span = time_span(i.add_time)
                i.last_reply = i.reply_set.order_by('-add_time')[:1]

        context = get_context()
        context['user'] = user
        context['topic_list'] = topic_list
        context['has_fav_user'] = has_fav_user

        return render(request, 'user-center.html', context)


class UserFavoriteView(LoginRequiredMixin, View):
    """用户收藏视图"""
    def get(self, request, fav_type):
        topic_list = []
        node_list = []
        text = ''
        if fav_type == 'topic':
            text = '收藏的主题'
            topic_id_list = [x.fav_id for x in UserFavorite.objects.filter(user=request.user, fav_type='topic')]
            topic_list = Topic.objects.filter(pk__in=topic_id_list).order_by('-add_time')
        elif fav_type == 'node':
            text = '收藏的节点'
            node_id_list = [x.fav_id for x in UserFavorite.objects.filter(user=request.user, fav_type='node')]
            node_list = Node.objects.filter(pk__in=node_id_list)
        elif fav_type == 'user':
            text = '关注的人的最新主题'
            user_id_list = [x.fav_id for x in UserFavorite.objects.filter(user=request.user, fav_type='user')]
            start = datetime.now() - timedelta(days=+14)
            print start
            topic_list = Topic.objects.filter(created_by__in=user_id_list, add_time__gt=start).order_by('-add_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(topic_list, 10, request=request)

        topic_list = p.page(page)

        if topic_list:
            for i in topic_list.object_list:
                i.time_span = time_span(i.add_time)
                i.last_reply = i.reply_set.order_by('-add_time')[:1]

        context = get_context()
        context['text'] = text
        context['fav_type'] = fav_type
        context['topic_list'] = topic_list
        context['node_list'] = node_list

        return render(request, 'user-favorite.html', context)


class UserSettingView(LoginRequiredMixin, View):
    """用户设置视图"""
    def get(self, request):
        context = get_context()
        return render(request, 'user-setting.html', context)

    def post(self, request):
        user_info = UserInfoForm(request.POST, instance=request.user)

        context = get_context()

        if user_info.is_valid():
            user_info.save()
            return render(request, 'user-setting.html', context)
        else:
            return render(request, 'user-setting.html', context)


class UploadImageView(LoginRequiredMixin, View):
    """用户头像上传"""
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponseRedirect(reverse('user:user_setting'))
        else:
            context = get_context()
            return render(request, 'user-setting.html', context)


class UpdatePwdView(LoginRequiredMixin, View):
    def post(self, request):
        password_old = request.POST.get('password_old')
        password_new = request.POST.get('password_new')
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            user = authenticate(username=request.user.username, password=password_old)
            if user:
                user.password = make_password(password_new)
                user.save()
                return HttpResponse(json.dumps({'success': True}), content_type='application/json')
            else:
                msg = '当前密码错误'
                return HttpResponse(json.dumps({'success': False, 'msg': msg}), content_type='application/json')
        else:
            msg = modify_form.errors['password_new']
            return HttpResponse(json.dumps({'success': False, 'msg': msg}), content_type='application/json')


def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response

