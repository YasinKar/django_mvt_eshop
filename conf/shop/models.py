from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(unique=True, max_length=200, verbose_name='دسته بندی')
    slug = models.SlugField(unique=True, allow_unicode=True, null=True, db_index=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True, db_index=True)
    image = models.ImageField(upload_to='categories', null=True, blank=True, verbose_name='عکس دسته بندی')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال', default=True, db_index=True)
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if self.parent and self.parent.parent:
            raise ValidationError('دسته‌بندی نمی‌تواند بیش از یک سطح زیرمجموعه داشته باشد.')
        
        if self.parent is None and not self.image:
            raise ValidationError('آپلود عکس برای دسته‌بندی‌های اصلی اجباری است.')
        
        if self.parent is not None and self.image:
            raise ValidationError('زیر دسته‌ها نیازی به عکس ندارند، لطفاً عکس را حذف کنید.')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.replace(' ', '-')
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        
class ProductTag(models.Model):
    tag = models.CharField(max_length=200, verbose_name='تگ')
    
    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'
        
    def __str__(self):
        return self.tag

class Brand(models.Model):
    name = models.CharField(unique=True, max_length=200, verbose_name='نام برند')
    logo = models.ImageField(upload_to='brands', verbose_name='لوگو برند')
    slug = models.SlugField(unique=True, allow_unicode=True, null=True, db_index=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال', default=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.replace(' ', '-')
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'
        
    def __str__(self):
        return self.name 

class ProductColor(models.Model):
    color = models.CharField(max_length=100, verbose_name='رنگ محصول')
    color_code = models.CharField(max_length=10, default='#fff', verbose_name='کد رنگ')
    
    def __str__(self):
        return self.color

    class Meta:
        verbose_name = 'رنگ بندی'
        verbose_name_plural = 'رنگ بندی محصولات'

class Product(models.Model):
    name = models.CharField(max_length=300, db_index=True, unique=True, verbose_name='نام محصول')
    slug = models.SlugField(unique=True, allow_unicode=True, null=True, db_index=True, blank=True)
    price = models.IntegerField(verbose_name='قیمت')
    image = models.ImageField(upload_to='products', verbose_name='تصویر')
    description = models.TextField(max_length=800, verbose_name='توضیحات')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='دسته بندی', db_index=True, related_name='products')
    colors = models.ManyToManyField(ProductColor, blank=True, verbose_name='رنگ های محصول')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='برند', db_index=True, related_name='products')
    tags = models.ManyToManyField(ProductTag, verbose_name='تگ های محصول', blank=True)
    inventory = models.IntegerField(
        default=1,
        verbose_name='تعداد موجودی',
        validators=[
            MaxValueValidator(1000),
            MinValueValidator(1)
        ]
    )
    is_sale = models.BooleanField(default=False, verbose_name='تخفیف')
    sale_price = models.IntegerField(verbose_name='قیمت در تخفیف', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال', default=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.replace(' ', '-')
        super().save(*args, **kwargs)
        
    def clean(self):
        if self.is_sale and not self.sale_price:
            raise ValidationError('قیمت در تخفیف نمیتواند خالی باشد.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['brand']),
            models.Index(fields=['is_active']),
        ]
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', related_name='images')
    image = models.ImageField(upload_to='products-gallery', verbose_name='تصویر')
    
    def __str__(self):
        return str(self.image)
    
    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصولات'
        
class ProductInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', related_name='informations')
    key = models.CharField(max_length=100, verbose_name='کلید')
    value = models.CharField(max_length=100, verbose_name='مقدار')
    
    def __str__(self):
        return f'{self.key} : {self.value}'
    
    class Meta:
        verbose_name = 'مشخصات'
        verbose_name_plural = 'مشخصات محصولات'
        
class ProductComment(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    message = models.TextField(verbose_name='متن دیدگاه')
    replay = models.ForeignKey(
    'self',
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    verbose_name='پاسخ',
    related_name='replies'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    recommend = models.BooleanField(default=True, verbose_name='توصیه میکنم / نمیکنم')
    date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='لایک ها')
    dislikes = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='دیس لایک ها')
    
    def save(self, *args, **kwargs):
        self.date = timezone.now()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'