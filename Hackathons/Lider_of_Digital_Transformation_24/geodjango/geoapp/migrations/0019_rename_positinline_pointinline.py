# Generated by Django 5.0 on 2023-12-22 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoapp', '0018_alter_positinline_mypoints'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PositInLine',
            new_name='PointInLine',
        ),
    ]
