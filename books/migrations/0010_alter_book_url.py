# Generated by Django 3.2.5 on 2023-09-24 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_auto_20230212_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='url',
            field=models.URLField(default=''),
        ),
    ]
