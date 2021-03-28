# 最是人间留不住,朱颜辞镜花辞树
# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^image_codes/(?P<uuid>[\w-]+)/$',views.ImageCodeView.as_view()),
]