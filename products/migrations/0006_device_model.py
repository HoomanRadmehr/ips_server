# Generated by Django 4.2 on 2023-05-11 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_device_brand_alter_device_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='model',
            field=models.CharField(default='abcd', max_length=50),
        ),
    ]
