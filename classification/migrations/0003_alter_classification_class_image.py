# Generated by Django 4.2 on 2023-04-20 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0002_alter_classification_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classification',
            name='class_image',
            field=models.ImageField(blank=True, upload_to='photos/classes'),
        ),
    ]
