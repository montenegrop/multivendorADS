# Generated by Django 3.1.4 on 2021-04-11 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0093_auto_20201130_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='language_code',
            field=models.CharField(default='es', max_length=35),
        ),
    ]
