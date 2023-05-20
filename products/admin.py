from django.contrib import admin
from products.models import Category,Brand,Device,DeviceSerial


admin.site.register([Category,Brand,Device,DeviceSerial])
