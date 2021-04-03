from django.db import DatabaseError
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.views import View
from django import http
import re,json,logging
from django.contrib.auth import login,logout,authenticate #authenticate为Django自己提供的登录校验
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from meiduo_mall.utlis.views import LoginRequiredJSONMixin

logger = logging.getLogger("django")
class EmailView(LoginRequiredJSONMixin,View):
    """保存用户的邮箱"""
    def put(self,request):
        """接收参数"""
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        email = json_dict.get("email")

        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code':1,'errmsg':"邮箱保存失败"})

        return http.JsonResponse({"code":0,"errmsg":"OK"})


class UserCenter(LoginRequiredMixin,View):
    def get(self,request):
        context = {
            "username":request.user.username,
            "mobile":request.user.mobile,
            "email":request.user.email,
            "email_active":request.user.email_active
        }
        return render(request,'user_center_info.html',context)


class LogoutView(View):
    def get(self,request):
        response = redirect(reverse("content:index"))
        #退出登录
        logout(request)
        response.delete_cookie("username")

        return response



class LoginUser(View):
    def get(self,request):
        return render(request,'login.html')


    def post(self,request):
        #后台校验,防止恶意用户
        username = request.POST.get("username")
        password = request.POST.get("password")
        remembered = request.POST.get("remembered")
        if not all([username,password]):
            return http.HttpResponseForbidden("缺少必传参数")

        if not re.match(r'[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20位的用户名')

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')

        user = authenticate(username = username,password = password)
        if user is None:
            return render(request,'login.html',{"account_errmsg":"账号或密码错误"})

        #状态保持
        login(request,user)
        if remembered != 'on':
            request.session.set_expiry(0)
        else:
            #默认两周
            request.session.set_expiry(None)
        next = request.GET.get("next")
        if next:
            response = redirect(next)

        else:
            response = redirect(reverse("content:index"))
        response.set_cookie('username',user.username,max_age=3600 * 24 * 15)
        return response



class UserNameCount(View):
    def get(self,request,username):
        count = User.objects.filter(username = username).count()
        return http.JsonResponse({"code":0,"errmsg":'OK','count':count})


class PhoneCount(View):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({"code":0,"errmsg":"OK","count":count})

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