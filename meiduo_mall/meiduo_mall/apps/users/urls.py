# 最是人间留不住,朱颜辞镜花辞树
# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views
urlpatterns = [
    #用户注册 reverse(users:register) == '/register/'
    url(r'^register/$',views.UsersView.as_view(),name='register'),
]
