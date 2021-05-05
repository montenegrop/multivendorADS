# Generated by Django 3.1.4 on 2021-05-05 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0009_auto_20210502_0634'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, default='AR', max_length=3)),
                ('province', models.CharField(blank=True, max_length=40)),
                ('city', models.CharField(blank=True, max_length=40)),
                ('postal_code', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='vendor',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendors.vendorlocation'),
        ),
    ]
