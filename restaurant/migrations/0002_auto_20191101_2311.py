# Generated by Django 2.2.6 on 2019-11-01 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menus',
            name='image',
            field=models.CharField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='menus',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='delivery_fee',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='free_delivery_threshold',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='lat',
            field=models.DecimalField(decimal_places=12, max_digits=15),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='lng',
            field=models.DecimalField(decimal_places=12, max_digits=15),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='logo_url',
            field=models.CharField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='restaurants',
            name='threshold',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.CreateModel(
            name='MenuCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('restaurant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.Restaurants')),
            ],
            options={
                'db_table': 'menucategories',
            },
        ),
        migrations.AddField(
            model_name='menus',
            name='menu_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.MenuCategories'),
        ),
    ]