# Generated by Django 4.0.3 on 2024-06-19 14:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('geoapp', '0068_alter_groups_start_alter_groups_stop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='stop',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
