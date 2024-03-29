# Generated by Django 4.2.10 on 2024-02-22 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_instantparik_created_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='instantparik',
            name='is_user_saved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='instantparik',
            name='parik',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.parik'),
        ),
    ]
