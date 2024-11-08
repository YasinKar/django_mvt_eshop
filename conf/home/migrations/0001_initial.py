# Generated by Django 5.0.7 on 2024-10-31 11:51

import home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='banners', verbose_name='عکس')),
                ('url', models.URLField(verbose_name='ادرس اسلایدر')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال / غیر فعال')),
            ],
            options={
                'verbose_name': 'بنر سایت',
                'verbose_name_plural': 'بنر',
            },
        ),
        migrations.CreateModel(
            name='SiteSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='sliders', verbose_name='عکس')),
                ('url', models.URLField(verbose_name='ادرس اسلایدر')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال / غیر فعال')),
            ],
            options={
                'verbose_name': 'اسلایدر سایت',
                'verbose_name_plural': 'اسلایدر',
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(upload_to='story_thumbnails', verbose_name='تامبنیل')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('video', models.FileField(upload_to='stories', validators=[home.models.validate_video_file], verbose_name='ویدیو')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال / غیر فعال')),
            ],
            options={
                'verbose_name': 'استوری',
                'verbose_name_plural': 'استوری ها',
            },
        ),
    ]
