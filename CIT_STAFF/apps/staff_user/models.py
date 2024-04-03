from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class OfficeChoices(models.TextChoices):
    HOD = 'HOD'
    UG = 'UG'
    PG = 'PG'
    TA = 'TA'
    
class RoleChoices(models.TextChoices):
    ADMINISTRATOR = 'Administrator'
    COORDINATOR = 'Coordinator'
    STAFF = 'Staff'
    
# Create your models here.
class StaffUser(AbstractUser):
    phone = models.CharField(max_length=20)
    office = models.CharField(max_length=30, choices=OfficeChoices)
    role = models.CharField(max_length=30, choices=RoleChoices)
    gender = models.CharField(choices=(('Male', 'Male'),('Female', 'Female')), max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table ='staff_user'