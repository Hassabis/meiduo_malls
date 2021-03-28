from django.db import DatabaseError
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.views import View
from django import http
import re
from django.contrib.auth import login
from users.models import User
# Create your views here.
class UserNameCount(View):
    def get(self,request,username):
        count = User.objects.filter(username = username).count()
        return http.JsonResponse({"code":0,"errmsg":'OK','count':count})


class UsersView(View):
    """用户注册"""
    def get(self,request):
        return render(request,'register.html')


    def post(self,request):
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        password2 = request.POST.get("cpwd")
        mobile = request.POST.get("phone")
        allow = request.POST.get("allow")
        #进行后端较校验
        if not all([username,password,password2,mobile,allow]):
            return http.HttpResponseForbidden('缺少参数')

        if not re.match(r'[a-zA-Z0-9_-]{5,20}$',username):
            return http.HttpResponseForbidden('请输入5-20位的用户名')

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')

        if allow != 'on':
            return http.HttpResponseForbidden('请勾选协议')

        # return render(request, 'register.html', {"register_errmes": "注册失败"})

        try:
            user = User.objects.create_user(username=username,password=password,mobile = mobile)
        except DatabaseError:
            return render(request,'register.html',{"register_errmes":"注册失败"})

        login(request,user)

        return redirect(reverse("content:index"))