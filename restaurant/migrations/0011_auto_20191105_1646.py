# Generated by Django 2.2.6 on 2019-11-05 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0010_auto_20191102_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menus',
            name='description',
            field=models.CharField(max_length=3000),
        ),
    ]