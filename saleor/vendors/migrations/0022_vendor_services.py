# Generated by Django 3.1.4 on 2021-05-27 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0150_auto_20210527_0410'),
        ('vendors', '0021_auto_20210517_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='services',
            field=models.ManyToManyField(blank=True, to='product.BaseProduct'),
        ),
    ]