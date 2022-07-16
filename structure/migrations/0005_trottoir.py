# Generated by Django 3.0 on 2021-07-01 13:51

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('structure', '0004_auto_20210630_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='trottoir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('Pvt', models.FloatField(blank=True, default=0.0, null=True)),
                ('b_rectangle', models.FloatField(default=0.0)),
                ('h_rectangle', models.FloatField(default=0.0)),
                ('pente', models.FloatField(default=0.0)),
                ('S_trottoir', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0.0), blank=True, null=True, size=None)),
                ('S_total_trottoir', models.FloatField(default=0.0)),
                ('L_trottoir', models.FloatField(default=0.0)),
                ('V_trottoir', models.FloatField(default=0.0)),
                ('P_trottoir', models.FloatField(default=0.0)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
            ],
        ),
    ]
