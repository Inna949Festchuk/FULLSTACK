# Generated by Django 4.0.3 on 2024-06-21 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoapp', '0078_alter_groups_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='result',
            field=models.DateTimeField(verbose_name='Время на маршруте'),
        ),
    ]