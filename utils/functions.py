from products.models import DeviceSerial
from datetime import timedelta
from django.utils import timezone


def is_valid_license(device_serial:DeviceSerial):
        duration = device_serial.license_exp
        created_at = device_serial.created_at
        if duration == '1y':
            expiration = created_at+timedelta(days=365)
        elif duration == '2y':
            expiration = created_at+timedelta(days=365*2)
        else:
            expiration = created_at+timedelta(days=365*3)
        if expiration>timezone.now():
            return True
        else:
            return None
        