# Generated by Django 4.2 on 2023-05-08 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_is_ordered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
    ]
