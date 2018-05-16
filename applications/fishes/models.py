from django.db import models
from .utils import image_rename
from django.utils import timezone
# Create your models here.


class FishPool(models.Model):
    '''鱼池信息表'''
    num = models.IntegerField(verbose_name='池子编号', unique=True)
    radius = models.FloatField(verbose_name='池子半径')
    depth = models.FloatField(verbose_name='池子深度')
    PH = models.FloatField(verbose_name='PH值')
    temperature = models.FloatField(verbose_name='温度')
    # fish_batch = models.IntegerField(verbose_name='鱼的批次', blank=True, null=True)
    in_using = models.BooleanField(verbose_name='是否正在使用中', default=False)

    def __str__(self):
        return self.num


class FishInfo(models.Model):
    '''鱼信息表'''
    fish_batch = models.CharField(verbose_name='鱼的批次号', max_length=20, unique=True)
    stock_date = models.DateTimeField(verbose_name='入料时间', default=timezone.now)
    number = models.IntegerField(verbose_name='鱼的数量')
    total_mass = models.FloatField(verbose_name='鱼的重量')
    name = models.CharField(verbose_name='品名', max_length=100)
    specification = models.CharField(verbose_name='规格', max_length=100)
    test_report_third = models.ImageField(verbose_name='第三方检测报告', upload_to=image_rename, null=True, blank=True)
    test_report_stock = models.ImageField(verbose_name='入料检测报告', upload_to=image_rename, null=True, blank=True)
    stock_scene = models.ImageField(verbose_name='入料情景', upload_to=image_rename, null=True, blank=True)
    is_stocking = models.BooleanField(verbose_name='是否正在存储中', default=True)
    is_processing = models.BooleanField(verbose_name='是否正在加工中', default=False)
    pool_num = models.ForeignKey(verbose_name='鱼池号', to=FishPool, related_name='fishinfo')

    def __str__(self):
        return self.fish_batch


class TransInfo(models.Model):
    '''转移记录表'''
    source_pool = models.ForeignKey(verbose_name='来源池', to=FishPool, related_name='source_pool')
    target_pool = models.ForeignKey(verbose_name='目的池', to=FishPool, related_name='target_pool')
    fish_info = models.ForeignKey(verbose_name='鱼的信息', to=FishInfo)
    tans_date = models.DateTimeField(verbose_name='转移日期', auto_created=True)

    def __str__(self):
        return str(self.source_pool) + " -> "+str(self.target_pool)


class ProcessInfo(models.Model):
    '''领料加工记录表'''
    fish_info = models.ForeignKey(verbose_name='鱼的信息', to=FishInfo)
    process_date = models.DateTimeField(verbose_name='加工日期', auto_created=True)
    process_environment = models.ImageField(verbose_name='加工情景', upload_to=image_rename, null=True, blank=True)
    pack_environment = models.ImageField(verbose_name='包装情景', upload_to=image_rename, null=True, blank=True)
    seal_environment = models.ImageField(verbose_name='封箱情景', upload_to=image_rename, null=True, blank=True)
    get_scene = models.ImageField(verbose_name='领料情景', upload_to=image_rename, null=True, blank=True)
    test_report_process = models.ImageField(verbose_name='加工检测报告', upload_to=image_rename, null=True, blank=True)


class QRCode(models.Model):
    '''二维码信息表'''
    qrcode = models.ImageField(verbose_name='二维码图片', upload_to=image_rename)
    fish_info = models.ForeignKey(verbose_name='鱼的信息', to=FishInfo)
    trans_info = models.ForeignKey(verbose_name='转移信息', to=TransInfo)
    process_info = models.ForeignKey(verbose_name='加工信息', to=ProcessInfo)



