# Generated by Django 2.2.17 on 2021-01-21 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0013_merge_20210120_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='regionalnetwork',
            field=models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.CASCADE, to='djangoldp_energiepartagee.Regionalnetwork', verbose_name='Paiement à effectuer à'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='managementcontact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Contact Gestion'),
        ),
    ]
