# Generated by Django 3.2.5 on 2022-07-30 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_book_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrecord',
            name='dateEnd',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='bookrecord',
            name='dateStart',
            field=models.DateTimeField(null=True),
        ),
    ]
