# Generated by Django 3.1.4 on 2021-06-17 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0026_socialmedia_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorAvatarImage',
            fields=[
                ('vendorgeneralimage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vendors.vendorgeneralimage')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avatar_image', to='vendors.vendor')),
            ],
            bases=('vendors.vendorgeneralimage', models.Model),
        ),
    ]
