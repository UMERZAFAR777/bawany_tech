# Generated by Django 5.1.6 on 2025-03-02 04:59

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_discount_alter_product_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_information',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
