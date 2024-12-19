# Generated by Django 5.0.7 on 2024-10-31 11:51

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='نام برند')),
                ('logo', models.ImageField(upload_to='brands', verbose_name='لوگو برند')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال / غیر فعال')),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برند ها',
            },
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100, verbose_name='رنگ محصول')),
                ('color_code', models.CharField(default='#fff', max_length=10, verbose_name='کد رنگ')),
            ],
            options={
                'verbose_name': 'رنگ بندی',
                'verbose_name_plural': 'رنگ بندی محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products-gallery', verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'تصویر محصول',
                'verbose_name_plural': 'تصاویر محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, verbose_name='کلید')),
                ('value', models.CharField(max_length=100, verbose_name='مقدار')),
            ],
            options={
                'verbose_name': 'مشخصات',
                'verbose_name_plural': 'مشخصات محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=200, verbose_name='تگ')),
            ],
            options={
                'verbose_name': 'تگ',
                'verbose_name_plural': 'تگ ها',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='دسته بندی')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories', verbose_name='عکس دسته بندی')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='فعال / غیر فعال')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.category')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=300, unique=True, verbose_name='نام محصول')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True)),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('image', models.ImageField(upload_to='products', verbose_name='تصویر')),
                ('description', models.TextField(max_length=800, verbose_name='توضیحات')),
                ('inventory', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(1)], verbose_name='تعداد موجودی')),
                ('is_sale', models.BooleanField(default=False, verbose_name='تخفیف')),
                ('sale_price', models.IntegerField(blank=True, null=True, verbose_name='قیمت در تخفیف')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='فعال / غیر فعال')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.brand', verbose_name='برند')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.category', verbose_name='دسته بندی')),
                ('colors', models.ManyToManyField(blank=True, to='shop.productcolor', verbose_name='رنگ های محصول')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('message', models.TextField(verbose_name='متن دیدگاه')),
                ('recommend', models.BooleanField(default=True, verbose_name='توصیه میکنم / نمیکنم')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')),
                ('likes', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='لایک ها')),
                ('dislikes', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='دیس لایک ها')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='shop.product', verbose_name='محصول')),
                ('replay', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='shop.productcomment', verbose_name='پاسخ')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
            },
        ),
    ]