from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_hope'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parik',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails'),
        ),
    ]
