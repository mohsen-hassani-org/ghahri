# Generated by Django 4.0.4 on 2022-05-30 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_alter_brand_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='booktime',
            name='locked',
            field=models.BooleanField(default=True, verbose_name='قفل شده'),
        ),
    ]