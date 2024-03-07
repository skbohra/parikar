# Generated by Django 5.0.1 on 2024-02-06 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_parik_shuffle_colors_by_line_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('font_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FontColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hexcode', models.CharField(max_length=7)),
            ],
        ),
    ]
