# Generated by Django 4.0.3 on 2024-06-06 15:58

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoapp', '0038_importtrek'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportInc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=' - ', max_length=250, verbose_name='Название инцидента')),
                ('location', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Импорт точек инцидента',
                'db_table': 'my_inc_model',
            },
        ),
        migrations.CreateModel(
            name='ImportTrekLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('azimuth', models.CharField(max_length=250)),
                ('pn', models.FloatField(default=0)),
                ('distance', models.CharField(max_length=250)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Местонахождение маршрута')),
            ],
            options={
                'verbose_name_plural': 'Создание линии по точкам',
                'db_table': 'trek_line_model',
            },
        ),
    ]