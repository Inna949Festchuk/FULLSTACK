# Generated by Django 4.0.3 on 2024-06-18 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoapp', '0061_groups_bool_stop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='id_group',
            field=models.IntegerField(default=False),
        ),
    ]
