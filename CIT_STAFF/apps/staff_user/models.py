from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class RoleChoices(models.TextChoices):
    ADMINISTRATOR = 'Administrator'
    ASSISTANT = 'Assistant'
    STAFF = 'Staff'
    RESEARCHER = 'Researcher'
    
# Create your models here.
class StaffUser(AbstractUser):
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=30, choices=RoleChoices)
    gender = models.CharField(choices=(('Male', 'Male'),('Female', 'Female')), max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table ='staff_user'