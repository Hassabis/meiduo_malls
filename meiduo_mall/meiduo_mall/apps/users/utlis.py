# 最是人间留不住,朱颜辞镜花辞树
# -*- coding:utf-8 -*-
from users.models import User
from django.contrib.auth.backends import ModelBackend
import re
def account_get_user(account):
    try:
        if re.match(r'1[3-9]\d{9}$', account):
            # 输入的是手机号
            user = User.objects.get(mobile=account)
        else:
            # 用户使用账号登录
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileBackends(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写用户认证的方法,使用户可以通过手机号或者账号去登录
        :param username:
        :param password:
        :param kwargs:
        :return:
        """
        user = account_get_user(username)
        if user and user.check_password(password):
            return user
        else:
            return None