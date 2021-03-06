# Generated by Django 2.2.6 on 2019-11-05 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinOrderMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Menus')),
            ],
            options={
                'db_table': 'join_order_menu',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_phone_number', models.CharField(max_length=15)),
                ('order_request', models.CharField(max_length=200)),
                ('delivery_fee', models.DecimalField(decimal_places=2, max_digits=8)),
                ('delivery_address', models.CharField(max_length=400)),
                ('created_at', models.DateTimeField(editable=False)),
                ('menus', models.ManyToManyField(through='order.JoinOrderMenu', to='restaurant.Menus')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.PaymentMethods')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Restaurants')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.AddField(
            model_name='joinordermenu',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order'),
        ),
    ]
