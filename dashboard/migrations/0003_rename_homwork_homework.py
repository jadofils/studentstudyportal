# Generated by Django 5.1.1 on 2024-09-06 16:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_homwork'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='homwork',
            new_name='Homework',
        ),
    ]
