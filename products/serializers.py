from rest_framework import serializers
from products.models import Category,Brand,Device,DeviceSerial
from rules.serializers import ListRuleSerializer
from user_manager.serializers import SimpleUserSerializer
from rules.models import Rule

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
    recommended_rules = ListRuleSerializer(read_only=True,many=True)
    
    class Meta:
        model = DeviceSerial
        fields = "__all__"
    
    def create(self, validated_data):
        return DeviceSerial.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    
class SellerSerialSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    creator = SimpleUserSerializer(read_only=True)
    owner = SimpleUserSerializer(read_only=True)
    
    class Meta:
        model = DeviceSerial
        fields = "__all__"
      
      
class AsignRuleSerializer(serializers.Serializer):
    rule_id = serializers.UUIDField()
    serial_id = serializers.UUIDField()
    
    def validate_rule_id(self,rule_id):
            rule = Rule.objects.filter(id=rule_id).last()
            if rule:
                if rule.is_verified:
                    return rule_id
                else:
                    raise serializers.ValidationError('rule is not verify')
            raise serializers.ValidationError("invalid rule")
        
    def validate_serial_id(self,serial_id):
        try:
            DeviceSerial.objects.get(id=serial_id)
            return serial_id
        except:
            raise serializers.ValidationError("invalid serial")
        