# Generated by Django 4.2 on 2023-05-14 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0003_rule_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='is_verifed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='rule',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
