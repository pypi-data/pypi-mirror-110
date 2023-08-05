# Generated by Django 2.2.19 on 2021-04-21 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0054_auto_20210419_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=25, max_digits=30, null=True, verbose_name='Lattitude'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='lng',
            field=models.DecimalField(blank=True, decimal_places=25, max_digits=30, null=True, verbose_name='Longitude'),
        ),
    ]
