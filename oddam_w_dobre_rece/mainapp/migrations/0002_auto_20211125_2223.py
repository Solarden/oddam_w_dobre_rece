# Generated by Django 3.2.9 on 2021-11-25 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='city_location',
            field=models.CharField(default='Warszawa', max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='institution',
            name='type',
            field=models.IntegerField(choices=[(1, 'Organizacja pozarządowa'), (0, 'Fundacja'), (2, 'Zbiórka lokalna')], default=0),
        ),
    ]
