# Generated by Django 4.0.4 on 2022-05-09 18:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(default=datetime.datetime.now, verbose_name='تاریخ')),
                ('time_in_day', models.CharField(choices=[('1400', '2:00 بعدازظهر'), ('1410', '2:10 بعدازظهر'), ('1420', '2:20 بعدازظهر'), ('1430', '2:30 بعدازظهر'), ('1440', '2:40 بعدازظهر'), ('1450', '2:50 بعدازظهر'), ('1500', '3:00 بعدازظهر'), ('1510', '3:10 بعدازظهر'), ('1520', '3:20 بعدازظهر'), ('1530', '3:30 بعدازظهر'), ('1540', '3:40 بعدازظهر'), ('1550', '3:50 بعدازظهر'), ('1600', '4:00 بعدازظهر'), ('1610', '4:10 بعدازظهر'), ('1620', '4:20 بعدازظهر'), ('1630', '4:30 بعدازظهر'), ('1640', '4:40 بعدازظهر'), ('1650', '4:50 بعدازظهر'), ('1700', '5:00 بعدازظهر'), ('1710', '5:10 بعدازظهر'), ('1720', '5:20 بعدازظهر'), ('1730', '5:30 بعدازظهر'), ('1740', '5:40 بعدازظهر'), ('1750', '5:50 بعدازظهر'), ('1800', '6:00 بعدازظهر'), ('1810', '6:10 بعدازظهر'), ('1820', '6:20 بعدازظهر'), ('1830', '6:30 بعدازظهر'), ('1840', '6:40 بعدازظهر'), ('1850', '6:50 بعدازظهر'), ('1900', '7:00 بعدازظهر'), ('1910', '7:10 بعدازظهر'), ('1920', '7:20 بعدازظهر'), ('1930', '7:30 بعدازظهر'), ('1940', '7:40 بعدازظهر'), ('1950', '7:50 بعدازظهر'), ('2000', '8:00 بعدازظهر'), ('2010', '8:10 بعدازظهر'), ('2020', '8:20 بعدازظهر'), ('2030', '8:30 بعدازظهر'), ('2040', '8:40 بعدازظهر'), ('2050', '8:50 بعدازظهر'), ('2100', '9:00 بعدازظهر'), ('2110', '9:10 بعدازظهر'), ('2120', '9:20 بعدازظهر'), ('2130', '9:30 بعدازظهر')], max_length=4, verbose_name='ساعت')),
            ],
            options={
                'verbose_name': 'زمان رزرو',
                'verbose_name_plural': 'زمان رزرو',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='نام برند')),
            ],
            options={
                'verbose_name': 'نام برند',
            },
        ),
        migrations.CreateModel(
            name='BrandCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='شرکت سازنده برند')),
            ],
            options={
                'verbose_name': 'شرکت سازنده برند',
                'verbose_name_plural': 'شرکت سازنده برند',
            },
        ),
        migrations.CreateModel(
            name='Illness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='نام بیماری')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
            ],
            options={
                'verbose_name': 'بیماری',
                'verbose_name_plural': 'بیماری',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='gallery/', verbose_name='تصویر')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('capture_time', models.IntegerField(choices=[(0, 'نامشخص'), (1, 'قبل از درمان'), (2, 'بعد از درمان'), (3, 'در مدت درمان')], default=0, verbose_name='زمان')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='نام دارو')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
            ],
            options={
                'verbose_name': 'دارو',
                'verbose_name_plural': 'دارو',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('visited_at', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ و ساعت مراجعه')),
                ('book_time', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', to='clinic.booktime', verbose_name='زمان رزرو')),
            ],
            options={
                'verbose_name': 'رزرو',
                'verbose_name_plural': 'رزرو',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='نام خدمت')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('price', models.IntegerField(verbose_name='قیمت (تومان)')),
            ],
            options={
                'verbose_name': 'خدمت',
                'verbose_name_plural': 'خدمت',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ReservationService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('service_brand', models.CharField(blank=True, max_length=255, null=True, verbose_name='برند خدمت')),
                ('service_amount', models.CharField(blank=True, max_length=100, null=True, verbose_name='میزان استفاده شده')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('final_price', models.DecimalField(decimal_places=0, max_digits=9, verbose_name='قیمت نهایی')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reservations', to='clinic.brand', verbose_name='برند')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='services', to='clinic.reservation', verbose_name='رزرو')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservation_services', to='clinic.service', verbose_name='خدمت')),
            ],
            options={
                'verbose_name': 'خدمت انجام شده',
                'verbose_name_plural': 'خدمت انجام شده',
            },
        ),
        migrations.CreateModel(
            name='ReservationMedicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('how_to_use', models.TextField(blank=True, null=True, verbose_name='نحوه استفاده')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', to='clinic.medicine', verbose_name='دارو')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medicines', to='clinic.reservation', verbose_name='رزرو')),
            ],
            options={
                'verbose_name': 'داروها',
                'verbose_name_plural': 'داروها',
            },
        ),
    ]