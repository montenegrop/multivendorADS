# Generated by Django 3.1.4 on 2021-06-10 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0023_auto_20210531_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorlocation',
            name='full_address',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
