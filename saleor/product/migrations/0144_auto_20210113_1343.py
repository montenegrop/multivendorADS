# Generated by Django 3.1.4 on 2021-01-13 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0143_auto_20210113_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id_simple',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
