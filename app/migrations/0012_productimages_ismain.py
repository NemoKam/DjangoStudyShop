# Generated by Django 4.1.3 on 2023-01-03 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_product_whcategory_product_whcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimages',
            name='ismain',
            field=models.BooleanField(default=False),
        ),
    ]
