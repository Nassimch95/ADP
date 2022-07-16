# Generated by Django 3.0 on 2021-07-02 23:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0014_auto_20210702_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablier',
            name='P_tablier',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0.0), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='tablier',
            name='P_tablier_sans_entretoise',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0.0), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='tablier',
            name='P_tablier_sans_entretoise_linear',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0.0), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='tablier',
            name='P_total_tablier',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='tablier',
            name='P_total_tablier_sans_entretoise',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='tablier',
            name='P_total_tablier_sans_entretoise_linear',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]