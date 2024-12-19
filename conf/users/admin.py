from django.contrib import admin
from . import models
from django.contrib.auth.models import Group

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone', 'email', 'date_joined', 'is_active']
    list_filter = ['first_name', 'last_name', 'username', 'phone', 'email', 'date_joined', 'is_active']
    list_editable = ['is_active']
    
admin.site.register(models.User, UserAdmin)

admin.site.unregister(Group)
