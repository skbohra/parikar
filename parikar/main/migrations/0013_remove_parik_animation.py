# Generated by Django 5.0.1 on 2024-02-06 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_parik_animation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parik',
            name='animation',
        ),
    ]
