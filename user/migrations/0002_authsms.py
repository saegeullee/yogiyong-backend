# Generated by Django 2.2.6 on 2019-11-06 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthSms',
            fields=[
                ('phone_number', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('auth_number', models.IntegerField()),
            ],
            options={
                'db_table': 'auth_numbers',
            },
        ),
    ]
