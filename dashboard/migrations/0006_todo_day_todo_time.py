# Generated by Django 5.1.1 on 2024-09-07 21:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='day',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='todo',
            name='time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]
