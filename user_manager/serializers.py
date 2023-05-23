from rest_framework.serializers import ModelSerializer
from user_manager.models import Users
from rest_framework.fields import CurrentUserDefault


def  get_user_serializer(request,*args,**kwargs):
    if request.user.is_superuser:
        return AdminUserSerializer(*args,**kwargs)
    elif request.user.is_installer:
        return InstallerUserSerializer(*args,**kwargs)
    elif request.user.is_supporter:
        return SupporterUserSerializer(*args,**kwargs)
    elif request.user.is_customer:
        return CustomerUserSerializer(*args,**kwargs)
    
class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','username','email','phone_number','created_by']

class AdminUserSerializer(ModelSerializer):
    created_by = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Users
        fields = "__all__"
    
    def create(self, validated_data):
        created_by = self.context['request'].user
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.created_by = created_by
        instance.save()
        
class SupporterUserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['username','email','is_active','created_by','date_joined','is_verified','phone_number']
    
        
class InstallerUserSerializer(ModelSerializer):
    created_by = SimpleUserSerializer(read_only=True)
    class Meta:
        model = Users
        fields = ['username','email','password','created_by','is_active','date_joined','is_verified','phone_number']
        
    def create(self,validated_data):
        created_by = self.context['request'].user
        instance = self.Meta.model(**validated_data)
        instance.set_password(validated_data['password'])
        instance.created_by = created_by
        instance.is_verified=False
        instance.is_installer=False
        instance.is_supporter=False
        instance.is_superuser=False
        instance.is_seller=False
        instance.is_customer=True
        validated_data.pop('password')
        instance.save()
        
class CustomerUserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['username','email','is_active','date_joined','is_verified','phone_number']
        