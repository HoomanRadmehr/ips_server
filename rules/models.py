from django.db import models
import uuid

    
class Rule(models.Model):
    ACTION_CHOICES = (('alert','alert'),('drop','drop'),('block','block'),('log','log'),('pass','pass'))
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    action = models.CharField(null=False,blank=False,default="alert",choices=ACTION_CHOICES)
    name = models.CharField(max_length=100,null=False,blank=False)
    code = models.TextField(null=False,blank=False)
    description = models.TextField(null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    version = models.FloatField(null=False,blank=True,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    