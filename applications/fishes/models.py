from django.db import models

# Create your models here.


class FishPool(models.Model):
    '''鱼池信息表'''
    num = models.IntegerField(verbose_name='池子编号', unique=True)
    radius = models.FloatField(verbose_name='池子半径')
    depth = models.FloatField(verbose_name='池子深度')
    PH = models.FloatField(verbose_name='PH值')
    temperature = models.FloatField(verbose_name='温度')
    fish_batch = models.IntegerField(verbose_name='鱼的批次', blank=True, null=True)