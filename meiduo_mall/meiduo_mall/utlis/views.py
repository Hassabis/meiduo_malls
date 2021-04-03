# 最是人间留不住,朱颜辞镜花辞树
# -*- coding:utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http

class LoginRequiredJSONMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        """重写未登录的处理逻辑"""
        return http.JsonResponse({"code":4401,'errmsg':'用户未登录'})