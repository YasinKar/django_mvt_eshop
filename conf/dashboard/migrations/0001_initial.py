# Generated by Django 5.0.7 on 2024-10-31 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('message', models.TextField(verbose_name='پیام')),
                ('date', models.DateField(auto_now_add=True, verbose_name='تاریخ')),
            ],
            options={
                'verbose_name': 'پیام',
                'verbose_name_plural': 'پیام ها',
            },
        ),
    ]
