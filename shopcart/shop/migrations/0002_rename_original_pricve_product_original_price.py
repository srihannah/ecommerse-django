# Generated by Django 5.0.7 on 2024-08-30 02:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='original_pricve',
            new_name='original_price',
        ),
    ]
