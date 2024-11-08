# Generated by Django 5.0.7 on 2024-10-31 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, verbose_name='شماره موبایل')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('message', models.TextField(verbose_name='پیام')),
                ('date', models.DateField(auto_now_add=True, verbose_name='تاریخ')),
            ],
            options={
                'verbose_name': 'تماس',
                'verbose_name_plural': 'تماس ها',
            },
        ),
        migrations.CreateModel(
            name='ElectronicSymbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='لینک')),
                ('image', models.ImageField(upload_to='e_symbols', verbose_name='عکس')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='فعال / غیر فعال')),
            ],
            options={
                'verbose_name': 'نماد الکترونیک',
                'verbose_name_plural': 'نمادهای الکترونیک',
            },
        ),
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=300, verbose_name='دامنه سایت')),
                ('site_name', models.CharField(max_length=100, verbose_name='نام سایت')),
                ('site_logo', models.ImageField(upload_to='site_logo', verbose_name='لوگو سایت')),
                ('site_icon', models.ImageField(blank=True, null=True, upload_to='site_icon', verbose_name='ایکون سایت')),
                ('site_about', models.TextField(verbose_name='درباره سایت')),
                ('adress', models.TextField(blank=True, null=True, verbose_name='ادرس')),
                ('rules', models.TextField(verbose_name='قوانین')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='شماره موبایل')),
                ('telegram', models.URLField(blank=True, max_length=400, null=True, verbose_name='ادرس کانال تلگرام')),
                ('instagram', models.URLField(blank=True, max_length=400, null=True, verbose_name='صفحه اینستاگرام')),
                ('email', models.CharField(blank=True, max_length=200, null=True, verbose_name='ایمیل')),
                ('copyright', models.CharField(default='&#169;کلیه حقوق محفوظ است', max_length=200, null=True, verbose_name='متن کپی رایت')),
                ('maintenance_mode', models.BooleanField(default=False, verbose_name='سایت فعال / غیر فعال')),
                ('is_main_setting', models.BooleanField(default=False, verbose_name='در نظر گرفن به عنوان تنظیمات اصلی')),
            ],
            options={
                'verbose_name': 'تنطیمات سایت',
                'verbose_name_plural': 'تنطیمات',
            },
        ),
    ]
