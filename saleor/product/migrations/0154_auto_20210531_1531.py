# Generated by Django 3.1.4 on 2021-05-31 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0153_auto_20210529_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastexperience',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.experiencelocation'),
        ),
        migrations.AlterField(
            model_name='pastexperience',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='past_experiences', to='product.product'),
        ),
    ]
