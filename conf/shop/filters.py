import django_filters
from .models import Brand, Product, Category, ProductColor

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='حداقل قیمت')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='حداکثر قیمت')
    is_sale = django_filters.BooleanFilter(label='تخفیف‌دار')
    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.filter(is_active=True), label='برند')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.filter(is_active=True), label='دسته‌بندی', method='filter_by_category')
    color = django_filters.ModelMultipleChoiceFilter(queryset=ProductColor.objects.all(), label='رنگ')
    
    ordering = django_filters.OrderingFilter(
        fields=(
            ('price', 'inexpensive'),
            ('-price', 'expensive'),
            ('id', 'newest'),
        ),
        field_labels={
            'price': 'مرتب‌سازی بر اساس قیمت',
            'id': 'مرتب‌سازی بر اساس جدید بودن',
        },
        label='مرتب‌سازی'
    )

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'is_sale', 'brand', 'category', 'color']
        
    def filter_by_category(self, queryset, name, value):
        if value:
            categories = [value] + list(Category.objects.filter(parent=value))
            return queryset.filter(category__in=categories)
        return queryset