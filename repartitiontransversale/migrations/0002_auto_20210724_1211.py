# Generated by Django 3.0 on 2021-07-24 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repartitiontransversale', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repartition_transversale',
            name='Ia',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='repartition_transversale',
            name='Im',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
