# 最是人间留不住,朱颜辞镜花辞树
# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views
urlpatterns = [
    #用户注册 reverse(users:register) == '/register/'
    url(r'^register/$',views.UsersView.as_view(),name='register'),
    #ajax
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',views.UserNameCount.as_view()),
    #ajax
    url(r'^phone/(?P<mobile>1[3-9]\d{9})/count/$',views.PhoneCount.as_view()),
    url(r'login/$',views.LoginUser.as_view(),name='login'),

    url(r'^logout/$',views.LogoutView.as_view(),name="logout"),
    url(r'^UserCenter/$',views.UserCenter.as_view(),name="UserCenters"),

    url(r'^emails/$',views.EmailView.as_view()),

]
