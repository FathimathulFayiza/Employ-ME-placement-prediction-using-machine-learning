# Generated by Django 3.2.18 on 2023-05-03 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PlacementPredictionApp', '0015_alter_performanceupdate_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='performanceupdate',
            name='field_value',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
