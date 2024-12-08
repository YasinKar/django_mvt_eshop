# Generated by Django 5.0.7 on 2024-10-31 11:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='productcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product', verbose_name='محصول'),
        ),
        migrations.AddField(
            model_name='productinformation',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='informations', to='shop.product', verbose_name='محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='shop.producttag', verbose_name='تگ های محصول'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='shop_produc_name_a2070e_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category'], name='shop_produc_categor_d249e3_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['brand'], name='shop_produc_brand_i_835a1f_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_active'], name='shop_produc_is_acti_2257ae_idx'),
        ),
    ]
