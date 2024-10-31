from django.contrib import admin
from . import models

class SiteSliderAdmin(admin.ModelAdmin):
    list_display = ['url', 'is_active']
    list_filter = ['url', 'is_active']
    list_editable = ['is_active']

class StoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['title', 'is_active']
    list_editable = ['is_active']

admin.site.register(models.Story, StoryAdmin)
admin.site.register(models.SiteSlider, SiteSliderAdmin)
admin.site.register(models.SiteBanner)