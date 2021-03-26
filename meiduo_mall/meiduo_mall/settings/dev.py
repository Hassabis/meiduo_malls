# 最是人间留不住,朱颜辞镜花辞树
# -*- coding:utf-8 -*-
"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%lgry9pgji-fx&o7)tp=a_9u5pg8)9&(b3py7jcmwv)msg62=7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        # 'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # 切换默认模板语言
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'environment':'meiduo_mall.utlis.jinja2_env.jinja2_environment',
        },
    },

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'meiduo_project',
        'HOST':'127.0.0.1',
        'USER':'root',
        'PASSWORD':'ITLiminary0610',
        'PORT':'3306',
    }
}
#配置Redis数据库
CACHES = {
    "default":{#默认的
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://127.0.0.1:6397/0",
        "OPTIONS":{
            "CLIENT_CLASS":"django_redis.client.DefaultClient",
        }
    },
    "session": {  # 默认的
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6397/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
#配置工程日志
LOGGING = {
    'version':1,
    'disable_existing_loggers':False,  #是否禁用已经存在的日志器
    'formatters':{
        'verbose':{
            'format':'%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple':{
            'format':'%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters':{#对日志进行过滤
        'require_debug_true':{
            '()':'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers':{
        'console':{ #向终端输出日志
            'level':'INFO',
            'filters':['require_debug_true'],
            'class':'logging.StreamHandler',
            'formatter':'simple'
        },
        'file':{
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join(os.path.dirname(BASE_DIR),'logs/meiduo.log'), #日志文件的位置
            'maxBytes':300 * 1024 * 1024,
            'backupCount':10,
            'formatter':'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端和文件中输出日志
            'propagate': True,  # 是否继续传输日志信息
            'level': 'INFO',  # 日志接收的最低级别
        },
    }
}