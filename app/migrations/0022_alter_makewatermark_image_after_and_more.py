# Generated by Django 4.1.3 on 2023-06-03 14:08

import app.models
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='makewatermark',
            name='image_after',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(app.models.pathAndRename, *(), **{'upload': 'afterWatermark/'})),
        ),
        migrations.AlterField(
            model_name='makewatermark',
            name='image_before',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(app.models.pathAndRename, *(), **{'upload': 'beforeWatermark/'})),
        ),
        migrations.AlterField(
            model_name='productimages',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(app.models.pathAndRename, *(), **{'upload': 'productImages/'})),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(app.models.pathAndRename, *(), **{'upload': 'profileAvatar/'})),
        ),
        migrations.AlterField(
            model_name='shop',
            name='image_url',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(app.models.pathAndRename, *(), **{'upload': 'shopAvatar/'})),
        ),
    ]
