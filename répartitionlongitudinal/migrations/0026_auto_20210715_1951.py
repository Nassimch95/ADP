# Generated by Django 3.0 on 2021-07-15 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('r√©partitionlongitudinal', '0025_auto_20210715_1759'),
    ]

    operations = [
        migrations.RenameField(
            model_name='repartition_longitudinal',
            old_name='M_Bc_TOTAL_UNE_VOIE_ET_N_VOIE',
            new_name='M_Bc_TOTAL',
        ),
        migrations.RemoveField(
            model_name='repartition_longitudinal',
            name='T_Bc_TOTAL_UNE_VOIE_ET_N_VOIE',
        ),
    ]
