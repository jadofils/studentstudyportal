# Generated by Django 5.1.1 on 2024-09-07 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_todo_day_todo_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='place',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
