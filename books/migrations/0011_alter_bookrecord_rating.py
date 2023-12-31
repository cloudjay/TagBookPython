# Generated by Django 3.2.5 on 2023-09-24 10:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_book_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrecord',
            name='rating',
            field=models.IntegerField(default=0, help_text='Stars', null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]
