# Generated by Django 3.1.4 on 2021-05-13 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0012_vendorimage_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]