# Generated by Django 3.1.4 on 2021-05-05 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0056_user_type_of_identification'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=35),
        ),
    ]