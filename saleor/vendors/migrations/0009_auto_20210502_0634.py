# Generated by Django 3.1.4 on 2021-05-02 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0008_auto_20210423_0551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='founding_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='total_employess',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
