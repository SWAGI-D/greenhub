# Generated by Django 5.2.4 on 2025-07-21 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_energyquiz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waterconservationsurvey',
            name='tap_off_while_brushing',
        ),
        migrations.AddField(
            model_name='waterconservationsurvey',
            name='turns_off_tap',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
