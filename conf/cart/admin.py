from django.contrib import admin
from . import models

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'is_paid', 'get_total_amount', 'paid_date')
    list_filter = ('status', 'is_paid')
    search_fields = ('user__username', 'address__address', 'user__phone')
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_paid=False)

# Register your models here.
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.OfferCode)