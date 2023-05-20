from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from user_manager.manager import UserManager
import uuid


class Users(AbstractUser):
    from products.validations import validate_device_id
    
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    username = models.CharField(("username"),max_length=150,unique=False,help_text=("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),validators=[AbstractUser.username_validator],null=True,blank=True)
    phone_number = models.CharField(max_length=25,null=True,blank=True)
    email = models.EmailField(max_length=254, unique=True)
    is_verified = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_supporter = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_installer = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["password"]
    