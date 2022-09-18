# Generated by Django 4.1.1 on 2022-09-17 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mobile', models.CharField(max_length=20, verbose_name='شماره تلفن')),
                ('template', models.CharField(max_length=255, verbose_name='قالب')),
                ('token1', models.CharField(blank=True, max_length=255, null=True, verbose_name='توکن اول')),
                ('token2', models.CharField(blank=True, max_length=255, null=True, verbose_name='توکن دوم')),
                ('token3', models.CharField(blank=True, max_length=255, null=True, verbose_name='توکن سوم')),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('response_text', models.CharField(blank=True, max_length=100, null=True, verbose_name='پاسخ درخواست')),
                ('response_code', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='کد پاسخ درخواست')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کارمند')),
            ],
            options={
                'verbose_name': 'تاریخچه پیامکی',
                'verbose_name_plural': 'تاریخچه پیامکی',
            },
        ),
    ]