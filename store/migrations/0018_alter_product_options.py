# Generated by Django 4.2 on 2023-05-27 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_product_dimensions_product_drive_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_date']},
        ),
    ]
