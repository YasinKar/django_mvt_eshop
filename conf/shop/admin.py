from django.contrib import admin
from . import models

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'inventory', 'category', 'brand', 'sale_price', 'is_sale', 'is_active']
    list_filter = ['name', 'price', 'inventory', 'category', 'brand', 'sale_price', 'is_sale', 'is_active']
    list_editable = ['is_active', 'is_sale']
    exclude = ['slug']
    search_fields = ('name', 'price', 'category__name', 'brand__name')
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['name', 'is_active']
    list_editable = ['is_active']
    exclude = ['slug']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['name', 'is_active']
    list_editable = ['is_active']
    exclude = ['slug']
    
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.ProductImage)
admin.site.register(models.ProductInformation)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductColor)
admin.site.register(models.ProductComment)