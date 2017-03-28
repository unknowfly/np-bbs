# _*_ coding:utf-8 _*_
import re

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from captcha.fields import CaptchaField

from .models import *


re_username = r'^[a-zA-Z0-9_]{4,16}$'
re_password = r'^[a-zA-Z0-9_]{6,16}$'
re_email = r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}'


class RegisterForm(forms.ModelForm):

    password_2 = forms.CharField(max_length=20, required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password']

    def clean(self):
        data = self.data
        username = data.get('username')
        password = data.get('password')
        password_2 = data.get('password_2')
        email = data.get('email')

        if not username:
            self._errors['username'] = self.error_class([u'用户名不能为空'])

        if not password:
            self._errors['password'] = self.error_class([u'密码不能为空'])

        if not email:
            self._errors['email'] = self.error_class([u'邮箱不能为空'])

        if password_2 != password:
            self._errors['password_2'] = self.error_class([u'两次输入密码不一致'])

        if not re.match(re_username, username):
            self._errors['username'] = self.error_class([u'用户名只能由4-16位的字母数字下划线组成'])

        if not re.match(re_password, password):
            self._errors['password'] = self.error_class([u'密码只能由6-16位的字母数字下划线组成'])

        if not re.match(re_email, email):
            self._errors['email'] = self.error_class([u'非法的邮箱格式'])

        if UserProfile.objects.filter(email=email):
            self._errors['email'] = self.error_class([u'该邮箱已经被注册'])

        if UserProfile.objects.filter(username=username):
            self._errors['username'] = self.error_class([u'用户名已经存在'])

        return data


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def clean(self):
        username = self.data.get('username')
        password = self.data.get('password')

        if not username:
            self._errors['username'] = self.error_class([u'登录名不能为空'])

        if not password:
            self._errors['password'] = self.error_class([u'密码不能为空'])

        return self.data


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birthday', 'gender', 'website', 'address']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class ModifyPwdForm(forms.Form):
    password_old = forms.CharField(required=True, min_length=5)
    password_new = forms.CharField(required=True, min_length=5)

    def clean(self):
        data = self.data
        password_old = data.get('password_old')
        password_new = data.get('password_new')

        if not password_old:
            self._errors['password_old'] = self.error_class([u'旧密码不能为空'])

        if not password_new:
            self._errors['password_new'] = self.error_class([u'新密码不能为空'])

        if not re.match(re_password, password_new):
            self._errors['password_new'] = self.error_class([u'密码只能由6-16位的字母数字下划线组成'])

        if password_old == password_new:
            self._errors['password_new'] = self.error_class([u'请输入一个新的密码'])

        return data


class ForgotPwdForm(forms.Form):
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})
    email = forms.EmailField(required=True, error_messages={'invalid': '请输入正确的邮箱地址'})

    def clean_email(self):
        email = self.data.get('email')
        if UserProfile.objects.filter(email=email):
            return email
        else:
            raise forms.ValidationError('未能找到该邮箱对应的用户')


class ResetPwdForm(forms.Form):
    password = forms.CharField(required=True)

    def clean(self):
        data = self.data
        password = data.get('password')

        if not password:
            self._errors['password'] = self.error_class([u'密码不能为空'])

        if not re.match(re_password, password):
            self._errors['password'] = self.error_class([u'密码只能由6-16位的字母数字下划线组成'])

        return data
