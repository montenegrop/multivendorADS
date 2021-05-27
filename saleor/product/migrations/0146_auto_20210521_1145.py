# Generated by Django 3.1.4 on 2021-05-21 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0145_category_relevance'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='base_products', to='product.category')),
                ('product_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='base_products', to='product.producttype')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='base_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.baseproduct'),
        ),
    ]