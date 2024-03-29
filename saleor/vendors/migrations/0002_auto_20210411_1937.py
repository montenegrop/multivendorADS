# Generated by Django 3.1.4 on 2021-04-11 19:37

from django.db import migrations, models
import saleor.core.utils.json_serializer


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='metadata',
            field=models.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='private_metadata',
            field=models.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='relevance',
            field=models.IntegerField(default=0),
        ),
    ]
