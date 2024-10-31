from django.db import models
from users.models import User
from shop.models import Product, ProductColor
from django.db.models import Case, When, F, DecimalField, Sum
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

class OfferCode(models.Model):
    code = models.CharField(max_length=150, verbose_name='کد تخفیف')
    discount_percentage = models.IntegerField(        
        verbose_name='درصد تخفیف',
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
    ])
    inventory = models.IntegerField(
        verbose_name='ظرفیت استفاده',
        default=10,
        validators=[
            MaxValueValidator(1000),
            MinValueValidator(1)
        ]
    )
    expiration_date = models.DateTimeField(verbose_name='تاریخ انقضا')

    def is_valid(self):
        if self.inventory is not None and self.inventory <= 0:
            return False
        if self.expiration_date and self.expiration_date < timezone.now():
            return False
        return True

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'
    
    def __str__(self):
        return self.code

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name= 'کاربر', related_name='addresses')
    receiver_first_name = models.CharField(max_length=200, verbose_name='نام گیرنده')
    receiver_last_name = models.CharField(max_length=200, verbose_name='نام خانوادگی گیرنده')
    phone = models.CharField(max_length=15, verbose_name='شماره موبایل گیرنده')
    national_code = models.CharField(max_length=10, verbose_name='کد ملی')
    post_code = models.CharField(max_length=10, verbose_name='کد پستی')
    address = models.TextField(verbose_name='نشانی گیرنده')
    province = models.CharField(max_length=300, verbose_name='استان')
    city = models.CharField(max_length=300, verbose_name='شهر')
    building_number = models.CharField(max_length=300, verbose_name='پلاک')
    building_unit = models.CharField(max_length=300, verbose_name='واحد')
    
    def __str__(self):
        return f'{self.receiver_first_name} {self.receiver_last_name}'
    
    def clean(self):
        phone_regex = r"^(0|98)?([ ]|-|[()]){0,2}9[0-4|9]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}$"
        if self.phone and not re.match(phone_regex, self.phone):
            raise ValidationError({'phone': 'شماره موبایل وارد شده معتبر نیست.'})
        
    class Meta:
        verbose_name = 'ادرس سفارش'
        verbose_name_plural = 'ادرس های سفارشات'
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name= 'کاربر', related_name='carts')
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='نشانی گیرنده')
    status = models.CharField(max_length=100, choices=(('در حال پردازش', 'در حال پردازش'), ('در حال تحویل', 'در حال تحویل'), ('تحویل داده شده', 'تحویل داده شده'), ('در انتظار پرداخت', 'در انتظار پرداخت')), verbose_name='وضعیت', default='در انتظار پرداخت')
    offer_code = models.ForeignKey(OfferCode, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='کد تخفیف')
    is_paid = models.BooleanField(default=False, verbose_name = 'پرداخت شده / نشده')
    paid = models.IntegerField(null=True, blank=True, verbose_name='مبلغ پرداخت شده')
    paid_date = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name='تاریخ پرداخت')
    
    def __str__(self):
        return self.user.username            
    
    def get_total_amount(self):
        total_amount = Order.objects.filter(cart=self).annotate(
            order_price=Case(
                When(product__is_sale=True, then=F('product__sale_price') * F('count')),
                default=F('product__price') * F('count'),
                output_field=DecimalField()
            )
        ).aggregate(total_amount=Sum('order_price'))['total_amount'] or 0
        
        if self.offer_code and self.offer_code.is_valid():
            discount_amount = (total_amount * self.offer_code.discount_percentage) / 100
            total_amount = total_amount - discount_amount
            
        return total_amount
    
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name = 'سبد خرید', related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = 'محصول')
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True, blank=True, verbose_name='رنگ')
    count = models.IntegerField(default=0, verbose_name= 'تعداد')
    
    def __str__(self):
        return str(self.cart)