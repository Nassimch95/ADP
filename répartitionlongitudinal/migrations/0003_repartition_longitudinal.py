# Generated by Django 3.0 on 2021-07-07 15:53

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
        ('r√©partitionlongitudinal', '0002_auto_20210707_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='repartition_longitudinal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('G', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), blank=True, size=None, unique=True), blank=True, size=None, unique=True)),
                ('A_TOTAL', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), blank=True, size=None, unique=True), blank=True, size=None, unique=True)),
                ('qtr_TOTAL', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), blank=True, size=None, unique=True), blank=True, size=None, unique=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
            ],
        ),
    ]
