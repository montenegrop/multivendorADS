# Generated by Django 3.1.4 on 2021-05-05 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0053_auto_20210505_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type_of_identification',
            field=models.CharField(blank=True, choices=[('empty', 'empty'), ('DNI', 'DNI'), ('pasaporte', 'pasaporte')], default='empty', max_length=30),
        ),
    ]
