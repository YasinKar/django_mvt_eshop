from django.contrib import admin
from . import models

class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'domain', 'is_main_setting', 'maintenance_mode']
    list_filter = ['site_name', 'domain', 'is_main_setting']
    list_editable = ['is_main_setting', 'maintenance_mode']
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['phone', 'title']
    list_filter = ['phone', 'title']
    
admin.site.register(models.SiteSetting, SiteSettingAdmin)
admin.site.register(models.ContactUs, ContactUsAdmin)
admin.site.register(models.ElectronicSymbol)