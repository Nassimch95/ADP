# Generated by Django 3.0 on 2021-06-30 15:17

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geometry', '0001_initial'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='poutre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('pvp', models.FloatField(default=0.0)),
                ('l_sa', models.FloatField(default=0.0)),
                ('cs_1', models.FloatField(default=0.0)),
                ('l_cs_1', models.FloatField(default=0.0)),
                ('l_si', models.FloatField(default=0.0)),
                ('cs_2', models.FloatField(default=0.0)),
                ('l_cs_2', models.FloatField(default=0.0)),
                ('l_sm', models.FloatField(default=0.0)),
                ('S', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0.0), blank=True, null=True, size=None)),
                ('L', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0.0), blank=True, null=True, size=None)),
                ('V', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0.0), blank=True, null=True, size=None)),
                ('vtp', models.FloatField(default=0.0)),
                ('np', models.FloatField(default=0.0)),
                ('ep', models.FloatField(default=0.0)),
                ('epdr', models.FloatField(default=0.0)),
                ('pp', models.FloatField(default=0.0)),
                ('ptp', models.FloatField(blank=True, default=0.0, null=True)),
                ('d_chevetre', models.FloatField(blank=True, default=0.5, null=True)),
                ('S_e', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0.0), blank=True, null=True, size=None)),
                ('S_e_total', models.FloatField(blank=True, default=0.0, null=True)),
                ('epaisseur_e', models.FloatField(blank=True, default=0.3, null=True)),
                ('V_e', models.FloatField(blank=True, default=0.0, null=True)),
                ('P_e', models.FloatField(blank=True, default=0.0, null=True)),
                ('pt_e', models.FloatField(blank=True, default=0.0, null=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
                ('sa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_about', to='geometry.SectionAdded')),
                ('si', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_intermediaire', to='geometry.SectionAdded')),
                ('sm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='section_mediane', to='geometry.SectionAdded')),
            ],
        ),
        migrations.CreateModel(
            name='corniche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('Pvc', models.FloatField(blank=True, default=0.0, null=True)),
                ('b_rectangle', models.FloatField(default=0.0)),
                ('h_rectangle', models.FloatField(default=0.0)),
                ('b_grand_triangle', models.FloatField(default=0.0)),
                ('h_grand_triangle', models.FloatField(default=0.0)),
                ('b_petit_triangle', models.FloatField(default=0.0)),
                ('h_petit_triangle', models.FloatField(default=0.0)),
                ('S_corniche', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(default=0.0), blank=True, null=True, size=None)),
                ('S_total_corniche', models.FloatField(default=0.0)),
                ('L_corniche', models.FloatField(default=0.0)),
                ('V_corniche', models.FloatField(default=0.0)),
                ('P_cornche', models.FloatField(default=0.0)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
            ],
        ),
    ]
