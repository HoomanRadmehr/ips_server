from rest_framework.serializers import ModelSerializer
from user_manager.models import Users

def get_user_serializer(request,*args,**kwargs):
    if request.user.is_superuser:
        return AdminUserSerializer(*args,**kwargs)
    elif request.user.is_installer:
        return InstallerUserSerializer(*args,**kwargs)
    elif request.user.is_supporter:
        return SupporterUserSerializer(*args,**kwargs)
    elif request.user.is_customer:
        return CustomerUserSerializer(*args,**kwargs)
    

class AdminUserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class SupporterUserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['username','email','is_active','date_joined','is_verified','phone_number','organization_number','address']
    
        
class InstallerUserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['username','email','is_active','date_joined','is_verified','phone_number','organization_number','address']
        
        
class CustomerUserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['username','email','is_active','date_joined','is_verified','phone_number','organization_number','address']
        
        
class SimpleUserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','username','email']
        