from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import re

class SiteSetting(models.Model):
    domain = models.CharField(max_length=300, verbose_name='دامنه سایت')
    site_name = models.CharField(max_length=100, verbose_name='نام سایت')
    site_logo = models.ImageField(upload_to='site_logo', verbose_name='لوگو سایت')
    site_icon = models.ImageField(upload_to='site_icon',null=True, blank=True, verbose_name='ایکون سایت')
    site_about = models.TextField(verbose_name='درباره سایت')
    adress = models.TextField(null=True, blank=True, verbose_name='ادرس')
    rules = models.TextField(verbose_name='قوانین')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='شماره موبایل')
    telegram = models.URLField(max_length=400, verbose_name='ادرس کانال تلگرام', null=True, blank=True)
    instagram = models.URLField(max_length=400, verbose_name='صفحه اینستاگرام', null=True, blank=True)
    email = models.CharField(max_length=200, verbose_name='ایمیل', null=True, blank=True)
    copyright = models.CharField(max_length=200, verbose_name='متن کپی رایت', null=True, default='&#169;کلیه حقوق محفوظ است')
    maintenance_mode = models.BooleanField(default=False, verbose_name='سایت فعال / غیر فعال')
    is_main_setting = models.BooleanField(default=False, verbose_name='در نظر گرفن به عنوان تنظیمات اصلی')
     
    class Meta:
        verbose_name = 'تنطیمات سایت'
        verbose_name_plural = 'تنطیمات'
    
    def __str__(self) :
        return self.site_name

    def clean(self):
        phone_regex = r"^(0|98)?([ ]|-|[()]){0,2}9[0-4|9]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}$"
        if self.phone and not re.match(phone_regex, self.phone):
            raise ValidationError({'phone': 'شماره موبایل وارد شده معتبر نیست.'})
    
class ElectronicSymbol(models.Model):
    url = models.URLField(max_length=200, verbose_name='لینک')
    image = models.ImageField(upload_to='e_symbols', verbose_name='عکس')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال', default=True, db_index=True)
     
    class Meta:
        verbose_name = 'نماد الکترونیک'
        verbose_name_plural = 'نمادهای الکترونیک'
   
class ContactUs(models.Model):
    phone = models.CharField(max_length=15, verbose_name='شماره موبایل')
    title = models.CharField(max_length=300, verbose_name='عنوان')
    message = models.TextField(verbose_name='پیام')
    date = models.DateField(auto_now_add=True, verbose_name='تاریخ')
    
    class Meta:
        verbose_name = 'تماس'
        verbose_name_plural = 'تماس ها'
    
    def __str__(self):
        return str(self.phone)
    
    def clean(self):
        phone_regex = r"^(0|98)?([ ]|-|[()]){0,2}9[0-4|9]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}$"
        if self.phone and not re.match(phone_regex, self.phone):
            raise ValidationError({'phone': 'شماره موبایل وارد شده معتبر نیست.'})
    
    def save(self, *args, **kwargs):
        self.date = timezone.now()
        super().save(*args, **kwargs)