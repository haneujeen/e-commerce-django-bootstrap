# Generated by Django 4.1.3 on 2022-11-21 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_remove_company_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(max_length=70),
        ),
    ]