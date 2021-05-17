# Generated by Django 3.1.4 on 2021-05-17 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0019_auto_20210517_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorcontact',
            name='role',
            field=models.CharField(choices=[('NONE', ''), ('sales', 'sales'), ('purchasing', 'purchasing'), ('indefinite', 'any')], default='NONE', max_length=30),
        ),
    ]
