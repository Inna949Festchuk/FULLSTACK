# Generated by Django 5.0 on 2023-12-30 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoapp', '0032_remove_worldline_name_remove_worldline_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='worldline',
            name='name',
            field=models.CharField(blank=True, default=' - ', max_length=250, verbose_name='Название схемы'),
        ),
    ]