# Generated by Django 3.2.9 on 2021-11-27 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20211125_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
    ]
