# Generated by Django 4.2.4 on 2023-11-03 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0003_orderpositions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='produsts',
        ),
    ]
