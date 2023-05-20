from django.core.exceptions import ValidationError


def validate_device_id(value):
    from products.models import DeviceSerial
    try:
        DeviceSerial.objects.get(id=str(value))
        return value
    except:
        raise ValidationError("This field accepts created device ids")