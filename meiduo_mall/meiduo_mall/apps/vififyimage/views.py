from django.shortcuts import render
from django.views import View
# Create your views here.
import captcha
from captcha.image import ImageCaptcha
import random
import string
from django_redis import get_redis_connection
from django import http

class ImageCodeView(View):

    def get(self,request,uuid):
        """
        uuid 作为唯一标识
        :param request:
        :param uuid:
        :return:image/jpg
        """
        image = ImageCaptcha(160, 60)  # 图片宽 160 高 60
        characters = string.digits + string.ascii_uppercase + string.ascii_lowercase  # 验证码组成，数字+大写字母+小写字母
        char_num = 4  # 验证码字符个数

        captcha_str = ''.join(random.sample(characters, char_num))
        # print(captcha_str)
        # img = image.generate_image(captcha_str) 这种方式生成的图片无法映射到网页
        img = image.generate(captcha_str) #这种方式生成的的图片无法保存
        # img.save(captcha_str + '.jpg')
        #将数据存入redis数据库，并且设置过期时间
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s'% uuid,300,captcha_str)

        #响应图形验证码
        return http.HttpResponse(img,content_type="image/jpg")


