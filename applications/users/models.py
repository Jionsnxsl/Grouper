from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class GrouperUser(AbstractUser):
    '''
    用户表(主要是指员工)
    '''
    employeeID = models.CharField(verbose_name="员工号", max_length=50)
    phoneNum = models.CharField(verbose_name='手机号', max_length=20)
    # username = models.CharField(verbose_name="用户名", max_length=50, null=False)
    # password = models.CharField(verbose_name="密码", max_length=100)
    # 约定：0---表示管理员；1---表示普通员工
    # permission = models.IntegerField(verbose_name="权限", null=False)

    def __str__(self):
        return self.username
