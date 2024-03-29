# Generated by Django 4.2.7 on 2024-01-14 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0006_rename_name_events_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='is_availabe',
        ),
        migrations.RemoveField(
            model_name='events',
            name='is_paid',
        ),
        migrations.AddField(
            model_name='events',
            name='ticketPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='events',
            name='ticketQuantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
