# Generated by Django 3.1.4 on 2021-05-27 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0149_auto_20210527_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastexperience',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.experiencelocation'),
        ),
    ]
