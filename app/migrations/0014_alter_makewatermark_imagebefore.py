# Generated by Django 4.1.3 on 2023-01-13 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_makewatermark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makewatermark',
            name='imagebefore',
            field=models.FileField(upload_to='media/beforeWatermark/'),
        ),
    ]
