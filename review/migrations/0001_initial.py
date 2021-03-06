# Generated by Django 2.2.6 on 2019-11-05 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('user', '0001_initial'),
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinReviewMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Menus')),
            ],
            options={
                'db_table': 'join_review_menu',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=300)),
                ('rating_taste', models.DecimalField(decimal_places=1, max_digits=2)),
                ('rating_delivery', models.DecimalField(decimal_places=1, max_digits=2)),
                ('rating_quantity', models.DecimalField(decimal_places=1, max_digits=2)),
                ('rating_avg', models.DecimalField(decimal_places=1, max_digits=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('menus', models.ManyToManyField(through='review.JoinReviewMenu', to='restaurant.Menus')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Restaurants')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_image', models.CharField(max_length=4000)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review.Review')),
            ],
            options={
                'db_table': 'review_images',
            },
        ),
        migrations.AddField(
            model_name='joinreviewmenu',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='review.Review'),
        ),
    ]
