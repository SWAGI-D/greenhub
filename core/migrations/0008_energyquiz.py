# Generated by Django 5.2.4 on 2025-07-21 03:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_sustainabilityentry'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EnergyQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn_off_lights', models.CharField(max_length=20)),
                ('efficient_appliances', models.CharField(max_length=20)),
                ('heating_cooling', models.CharField(max_length=20)),
                ('unplug_devices', models.CharField(max_length=20)),
                ('renewable_energy', models.CharField(max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
