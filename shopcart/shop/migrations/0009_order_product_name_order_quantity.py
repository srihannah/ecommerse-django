# Generated by Django 5.0.7 on 2024-09-07 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_name',
            field=models.CharField(default='Unknown Product', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]