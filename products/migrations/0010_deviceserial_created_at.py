# Generated by Django 4.2 on 2023-05-14 06:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_deviceserial_owner_alter_deviceserial_creator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserial',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
