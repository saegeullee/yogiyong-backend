# Generated by Django 2.2.6 on 2019-11-05 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_auto_20191105_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menus',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='address',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='company_name',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='delivery_fee_explanation',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='name',
            field=models.CharField(max_length=500),
        ),
    ]
