# Generated by Django 4.0.5 on 2022-06-19 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_marriage_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='users/avatars', verbose_name='تصویر پروفایل'),
        ),
    ]
