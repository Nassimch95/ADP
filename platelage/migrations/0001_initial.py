# Generated by Django 3.0 on 2021-08-06 18:42

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
        ('repartitiontransversale', '0008_auto_20210801_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='platelage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('u0', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, max_length=10), blank=True, null=True, size=None), blank=True, null=True, size=None)),
                ('u1', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, max_length=10), blank=True, null=True, size=None), blank=True, null=True, size=None)),
                ('ua', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, max_length=10), blank=True, null=True, size=None), blank=True, null=True, size=None)),
                ('u0_3teta', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, max_length=10), blank=True, null=True, size=None), blank=True, null=True, size=None)),
                ('u1_3teta', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, max_length=10), blank=True, null=True, size=None), blank=True, null=True, size=None)),
                ('ua_3teta', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, max_length=10), blank=True, null=True, size=None), blank=True, null=True, size=None)),
                ('matrice_teta_p', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, max_length=10), blank=True, null=True, size=None), blank=True, null=True, size=None)),
                ('matrice_teta_n', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, max_length=10), blank=True, null=True, size=None), blank=True, null=True, size=None)),
                ('matrice_3teta_p', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, max_length=10), blank=True, null=True, size=None), blank=True, null=True, size=None)),
                ('matrice_3teta_n', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, max_length=10), blank=True, null=True, size=None), blank=True, null=True, size=None)),
                ('R_transversale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repartitiontransversale.repartition_transversale')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
            ],
        ),
    ]