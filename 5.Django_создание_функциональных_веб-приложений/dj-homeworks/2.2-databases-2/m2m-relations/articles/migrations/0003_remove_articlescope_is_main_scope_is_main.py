# Generated by Django 4.2.7 on 2023-11-09 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_scope_alter_article_options_articlescope_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlescope',
            name='is_main',
        ),
        migrations.AddField(
            model_name='scope',
            name='is_main',
            field=models.BooleanField(default=False),
        ),
    ]
