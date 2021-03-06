# Generated by Django 2.2.6 on 2019-11-05 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='MenuCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'menucategories',
            },
        ),
        migrations.CreateModel(
            name='Restaurants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=100)),
                ('lat', models.DecimalField(decimal_places=12, max_digits=15)),
                ('lng', models.DecimalField(decimal_places=12, max_digits=15)),
                ('phone_order', models.BooleanField(default=False, null=True)),
                ('free_delivery_threshold', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('delivery_fee_explanation', models.CharField(max_length=500, null=True)),
                ('threshold', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('logo_url', models.URLField(max_length=4000, null=True)),
                ('estimated_delivery_time', models.CharField(max_length=20, null=True)),
                ('city', models.CharField(max_length=20)),
                ('review_count', models.IntegerField(null=True)),
                ('open_time_description', models.CharField(max_length=100, null=True)),
                ('additional_discount', models.IntegerField(null=True)),
                ('review_image_count', models.IntegerField(null=True)),
                ('is_available_pickup', models.BooleanField(null=True)),
                ('delivery_fee', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('review_avg', models.DecimalField(decimal_places=1, max_digits=2, null=True)),
                ('one_dish', models.BooleanField(null=True)),
                ('ingredients_origin', models.TextField(null=True)),
                ('company_name', models.CharField(max_length=500, null=True)),
                ('company_number', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'restaurants',
            },
        ),
        migrations.CreateModel(
            name='Restaurants_Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.Restaurants')),
            ],
            options={
                'db_table': 'restaurants_tags',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('restaurant', models.ManyToManyField(through='restaurant.Restaurants_Tags', to='restaurant.Restaurants')),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.AddField(
            model_name='restaurants_tags',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.Tags'),
        ),
        migrations.CreateModel(
            name='Restaurants_Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.Categories')),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.Restaurants')),
            ],
            options={
                'db_table': 'restaurants_categories',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Restaurants')),
            ],
            options={
                'db_table': 'payment_methods',
            },
        ),
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=3000)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('quantity', models.IntegerField()),
                ('image', models.URLField(max_length=4000, null=True)),
                ('menu_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.MenuCategories')),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.Restaurants')),
            ],
            options={
                'db_table': 'menus',
            },
        ),
        migrations.AddField(
            model_name='menucategories',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.Restaurants'),
        ),
        migrations.AddField(
            model_name='categories',
            name='restaurant',
            field=models.ManyToManyField(through='restaurant.Restaurants_Categories', to='restaurant.Restaurants'),
        ),
    ]
