# Generated by Django 2.2.6 on 2019-11-01 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20191030_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email_accept',
            new_name='notification_accept',
        ),
    ]
