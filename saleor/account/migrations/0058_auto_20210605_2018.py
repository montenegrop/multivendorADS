# Generated by Django 3.1.4 on 2021-06-05 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0023_auto_20210531_1541'),
        ('account', '0057_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='vendors.vendor'),
        ),
    ]
