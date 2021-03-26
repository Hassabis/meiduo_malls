# 最是人间留不住,朱颜辞镜花辞树
# -*- coding:utf-8 -*-
from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
def jinja2_environment(**options):
    """
    创建jinji2环境
    :param options:
    :return:
    """
    env = Environment(**options)
    #自定义语法{{ static('静态文件相对路径') }} {{ url('路由命名空间') }}
    env.globals.update({
        'static':staticfiles_storage.url, #加载静态文件的前缀
        'url':reverse, #反向解析
    })
    #返回环境对象
    return env
