# Generated by Django 5.0.7 on 2024-08-31 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_rename_original_pricve_product_original_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Catagory',
            new_name='Category',
        ),
    ]