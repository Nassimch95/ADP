# Generated by Django 3.0 on 2021-07-29 19:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repartitiontransversale', '0005_auto_20210729_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='repartition_transversale',
            name='p1_A_2V',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, max_length=10), blank=True, null=True, size=None), blank=True, null=True, size=None),
        ),
    ]
