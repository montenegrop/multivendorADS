# Generated by Django 3.1.4 on 2021-05-27 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0148_auto_20210527_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastexperience',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='past_experiences', to='product.product'),
        ),
    ]
