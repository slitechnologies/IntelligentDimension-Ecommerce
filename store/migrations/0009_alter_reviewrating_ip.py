# Generated by Django 4.2 on 2023-05-10 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_reviewrating_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='ip',
            field=models.CharField(max_length=20),
        ),
    ]