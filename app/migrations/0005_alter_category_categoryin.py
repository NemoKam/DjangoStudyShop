# Generated by Django 4.1.3 on 2022-11-23 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_category_categoryin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categoryin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categ', to='app.category'),
        ),
    ]
