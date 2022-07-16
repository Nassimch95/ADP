# Generated by Django 3.0 on 2021-06-30 15:41

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0002_remove_corniche_s_corniche'),
    ]

    operations = [
        migrations.AddField(
            model_name='corniche',
            name='S_corniche',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0.0), blank=True, null=True, size=None),
        ),
    ]
