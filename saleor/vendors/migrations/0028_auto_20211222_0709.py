# Generated by Django 3.1.4 on 2021-12-22 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0027_vendoravatarimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='cuit',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='vendor',
            name='razon_social',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
