# Generated by Django 2.2 on 2020-08-04 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_order_order_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
    ]