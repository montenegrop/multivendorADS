# Generated by Django 3.1.4 on 2021-05-11 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0011_auto_20210511_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorimage',
            name='title',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
