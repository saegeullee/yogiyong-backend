# Generated by Django 2.2.6 on 2019-11-03 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20191103_0039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewimage',
            old_name='review_imgae',
            new_name='review_image',
        ),
        migrations.AlterField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
    ]