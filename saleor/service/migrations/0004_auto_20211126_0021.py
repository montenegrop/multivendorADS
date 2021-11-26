# Generated by Django 3.1.4 on 2021-11-26 00:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20211014_0345'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecontract',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='servicecontract',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
