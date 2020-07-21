# Generated by Django 2.2 on 2020-07-21 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20200720_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Section name'),
        ),
        migrations.AlterField(
            model_name='section',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Slug'),
        ),
    ]