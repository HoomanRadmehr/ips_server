# Generated by Django 4.2 on 2023-05-17 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0004_rule_is_verifed_alter_rule_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='version',
            field=models.FloatField(blank=True, default=1),
        ),
    ]
