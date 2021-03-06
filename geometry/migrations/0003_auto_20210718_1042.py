# Generated by Django 3.0 on 2021-07-18 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geometry', '0002_auto_20210718_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section_type_01',
            name='IG_avec_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_01',
            name='IG_sans_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_01',
            name='V_avec_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_01',
            name='V_prime_avec_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_01',
            name='V_prime_sans_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_01',
            name='V_sans_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_01',
            name='rendement_avec_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_01',
            name='rendement_sans_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_02',
            name='IG_avec_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_02',
            name='IG_sans_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_02',
            name='V_avec_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_02',
            name='V_prime_avec_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_02',
            name='V_prime_sans_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_02',
            name='V_sans_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_02',
            name='rendement_avec_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='section_type_02',
            name='rendement_sans_hourdis',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
