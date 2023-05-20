from rest_framework import serializers
from products.models import Category,Brand,Device,DeviceSerial
from user_manager.serializers import SimpleUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class DeviceSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    class Meta:
        model = Device
        fields = "__all__"
        
class DeviceCreateSerializer(serializers.Serializer):
    brand_id = serializers.UUIDField()
    category_id = serializers.UUIDField()
    description = serializers.CharField()
    
    def create(self, validated_data):
        return Device.objects.create(**validated_data)
    
class SerialSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    creator = SimpleUserSerializer(read_only=True)
    owner = SimpleUserSerializer(read_only=True)
    
    class Meta:
        model = DeviceSerial
        fields = "__all__"
    
    def create(self, validated_data):
        return DeviceSerial.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    