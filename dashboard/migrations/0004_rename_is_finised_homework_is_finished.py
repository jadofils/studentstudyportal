# Generated by Django 5.1.1 on 2024-09-07 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_rename_homwork_homework'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homework',
            old_name='is_finised',
            new_name='is_finished',
        ),
    ]
