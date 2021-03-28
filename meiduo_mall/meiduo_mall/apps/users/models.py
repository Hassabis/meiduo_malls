from django.db import models
from django.contrib.auth.models import AbstractUser #使用Django自带的用户处理系统
# Create your models here.
class User(AbstractUser):
    #在拥有父类的用户属性后增加自己的字段
    #在迁移前记得去global_settings里面将AUTH_USER_MODEL = 'users.User'复制到配置文件里，#指定自定义的用户模型类 值的语法 ==> '子应用.用户模型类'
    mobile = models.CharField(max_length=12,unique=True,verbose_name="手机号")

    class Meta:
        db_table = 'db_user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name