# Generated by Django 4.0.4 on 2022-05-09 18:38

import apps.users.managers
import apps.users.validators
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clinic', '0001_initial'),
        ('core', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mobile', models.CharField(error_messages={'unique': 'این شماره موبایل از قبل در سامانه ثبت شده است'}, help_text='موبایل باید به فرمت 09123456789 وارد شود', max_length=11, unique=True, validators=[apps.users.validators.MobileValidator()], verbose_name='موبایل')),
                ('password', models.CharField(blank=True, max_length=128, null=True, verbose_name='گذرواژه')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='نام خانوادگی')),
                ('national_code', models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[apps.users.validators.NationalCodeValidator()], verbose_name='کد ملی')),
                ('deactivate_reason', models.PositiveSmallIntegerField(choices=[(0, 'نامشخص'), (1, 'غیر فعال توسط مدیر'), (2, 'غیر فعال توسط کارمندان'), (3, 'عدم تایید موبایل'), (4, 'عدم تایید ایمیل')], default=0, verbose_name='غیرفعال به دلیل')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='ایمیل')),
                ('address', models.TextField(blank=True, null=True, verbose_name='آدرس')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('gender', models.IntegerField(blank=True, choices=[(0, 'مرد'), (1, 'زن')], null=True, verbose_name='جنسیت')),
                ('role', models.IntegerField(choices=[(0, 'مدیر'), (1, 'دکتر'), (2, 'منشی'), (3, 'بیمار')], default=3, verbose_name='نقش')),
                ('marriage_status', models.IntegerField(choices=[(0, 'مجرد'), (1, 'متاهل')], default=0, verbose_name='وضعیت تاهل')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='شماره تلفن ثابت')),
                ('treatment_history', models.TextField(blank=True, null=True, verbose_name='سوابق درمانی')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
                ('referral_code', models.CharField(default=None, max_length=10, null=True, unique=True, verbose_name='کد معرف')),
                ('career', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='core.career', verbose_name='شغل')),
                ('current_illness', models.ManyToManyField(blank=True, related_name='patients', to='clinic.illness', verbose_name='بیماری های فعلی')),
                ('current_medicines', models.ManyToManyField(blank=True, related_name='patients', to='clinic.medicine', verbose_name='داروهای مصرفی فعلی')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربر',
                'ordering': ('-id',),
            },
            managers=[
                ('objects', apps.users.managers.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('referred', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='referral_by', to=settings.AUTH_USER_MODEL, verbose_name='گاربر معرفی شده')),
                ('referrer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='referrals', to=settings.AUTH_USER_MODEL, verbose_name='ارجاع دهنده')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
