# Generated by Django 4.2.10 on 2024-02-19 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_parik_font_size_instantparik'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instantparik',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
