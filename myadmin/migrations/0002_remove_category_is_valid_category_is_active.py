# Generated by Django 4.2.7 on 2023-11-20 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_valid',
        ),
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
