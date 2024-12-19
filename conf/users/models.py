from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from . managers import CustomUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone
import random, re

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']
    
    def clean(self):
        phone_regex = r"^(0|98)?([ ]|-|[()]){0,2}9[0-4|9]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}$"
        if self.phone and not re.match(phone_regex, self.phone):
            raise ValidationError({'phone': 'شماره موبایل وارد شده معتبر نیست.'})
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

class OTP(models.Model):
    phone = models.CharField(max_length=15, verbose_name='شماره موبایل')
    otp = models.CharField(max_length=6, verbose_name='کد یکبار مصرف')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    
    def clean(self):
        phone_regex = r"^(0|98)?([ ]|-|[()]){0,2}9[0-4|9]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}$"
        if not re.match(phone_regex, self.phone):
            raise ValidationError({'phone': 'شماره موبایل وارد شده معتبر نیست.'})

    def is_valid(self):
        return self.created_at >= timezone.now() - timezone.timedelta(minutes=2)

    def generate_otp(self):
        self.otp = str(random.randint(10000, 99999))
        self.created_at = timezone.now()
        self.save()
        return self.otp
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # first save new record
        # delete old otp records
        if OTP.objects.count() > 100:
            excess = OTP.objects.order_by('created_at')[:OTP.objects.count() - 100]
            for otp in excess:
                otp.delete()
    
    def __str__(self):
        return self.phone
    
    class Meta:
        verbose_name = 'کد یکبار مصرف'
        verbose_name_plural = 'کد های یکبار مصرف'