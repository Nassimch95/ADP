# Generated by Django 3.0 on 2021-07-03 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0015_auto_20210703_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='poutre',
            name='pve',
            field=models.FloatField(blank=True, null=True),
        ),
    ]