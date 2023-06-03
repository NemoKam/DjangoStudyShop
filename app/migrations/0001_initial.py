# Generated by Django 4.1.3 on 2022-11-23 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('categoryin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('imageUrl', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('images', models.TextField()),
                ('amount', models.IntegerField()),
                ('price', models.IntegerField()),
                ('active', models.BooleanField()),
                ('whcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
                ('whshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.shop')),
            ],
        ),
    ]
