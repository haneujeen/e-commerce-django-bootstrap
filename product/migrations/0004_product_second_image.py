# Generated by Django 4.1.3 on 2022-11-09 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_company_company_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='second_image',
            field=models.ImageField(blank=True, upload_to='product/images/%Y/%m/%d/'),
        ),
    ]
