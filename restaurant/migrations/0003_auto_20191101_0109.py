# Generated by Django 2.2.6 on 2019-10-31 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20191031_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
