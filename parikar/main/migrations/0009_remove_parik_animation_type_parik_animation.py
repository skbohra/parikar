# Generated by Django 5.0.1 on 2024-02-06 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_animation_alter_parik_animation_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parik',
            name='animation_type',
        ),
        migrations.AddField(
            model_name='parik',
            name='animation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.animation'),
            preserve_default=False,
        ),
    ]
