# Generated by Django 2.2.6 on 2019-11-07 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_authsms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='social_platform',
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, null=True),
        ),
    ]