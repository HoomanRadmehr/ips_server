from django.db import models
from rules.models import Rule
import uuid

class Category(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    name = models.CharField(null=False,blank=False,unique=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    name = models.CharField(null=False,blank=False,unique=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self) -> str:
        return self.name

class Device(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    category = models.ForeignKey(Category,related_name="category",on_delete=models.CASCADE,null=True,blank=True)
    brand = models.ForeignKey(Brand,related_name="brand",on_delete=models.CASCADE,null=True,blank=True)
    model = models.CharField(max_length=50,null=False,blank=False,default="abcd")
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    
    def __str__(self) -> str:
        return f"{self.brand}-{self.model}"
    
    class Meta:
        unique_together = ("category","brand")
        
class DeviceSerial(models.Model):
    from user_manager.models import Users
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    device = models.ForeignKey(Device,on_delete=models.DO_NOTHING,null=False,blank=False)
    creator = models.ForeignKey(Users,on_delete=models.DO_NOTHING,null=False,blank=True,related_name="serial_creator")
    owner = models.ForeignKey(Users,on_delete=models.DO_NOTHING,null=True,blank=True,related_name="device_owner")
    recommended_rules = models.ManyToManyField(Rule,related_name='rules_serial')
    address = models.TextField(null=True,blank=True)
    organization_number = models.CharField(max_length=25,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)
    