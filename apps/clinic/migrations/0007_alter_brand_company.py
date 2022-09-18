# Generated by Django 4.0.5 on 2022-06-19 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0006_rename_service_amount_reservationservice_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='brands', to='clinic.brandcompany', verbose_name='شرکت'),
        ),
    ]