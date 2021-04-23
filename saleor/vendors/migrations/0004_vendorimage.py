# Generated by Django 3.1.4 on 2021-04-22 17:53

from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_vendor_main_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(db_index=True, editable=False, null=True)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, upload_to='vendors')),
                ('ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20)),
                ('alt', models.CharField(blank=True, max_length=128)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='vendors.vendor')),
            ],
            options={
                'ordering': ('sort_order', 'pk'),
            },
        ),
    ]