# Generated by Django 4.2 on 2023-05-13 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0008_alter_deviceserial_creator_alter_deviceserial_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceserial',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='device_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='deviceserial',
            name='creator',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='serial_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='deviceserial',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.device'),
        ),
    ]