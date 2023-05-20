from django_filters import rest_framework as filters
from products.models import Category,Brand,Device,DeviceSerial


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ('name','created_at')
        

class BrandFilter(filters.FilterSet):
    class Meta:
        model = Brand
        fields = ('name','created_at')
        
        
class DeviceFilter(filters.FilterSet):
    class Meta:
        model = Device
        fields = ('category_id','brand_id','created_at')
        
    
class SerialFilter(filters.FilterSet):
    class Meta:
        model = DeviceSerial
        fields = ('owner_id','device_id','creator_id','created_at')
        