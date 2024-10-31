from django.db import models
from users.models import User
from django.utils import timezone

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='messages')
    title = models.CharField(max_length=300, verbose_name='عنوان')
    message = models.TextField(verbose_name='پیام')
    date = models.DateField(auto_now_add=True, verbose_name='تاریخ')
    
    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'
    
    def __str__(self):
        return self.user.username