from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class OfficeChoices(models.TextChoices):
    HOD = 'HOD'
    UG = 'Under Graduate'
    PG = 'Post Graduate'
    DEVELOPER = 'Developer'
    
class RoleChoices(models.TextChoices):
    ADMINISTRATOR = 'Administrator'
    COORDINATOR = 'Coordinator'
    STAFF = 'Staff'
    HEAD = 'Head'
    
class WorkRoleChoices(models.TextChoices):
    ASSISTANT = 'Assistant'
    LECTURER = 'Lecturer'
    SECRETARY = 'Secretary'
    
class SectionChoices(models.TextChoices):
    CSE = 'Computer Science and Engineering'
    CE = 'Computer Engineering'
    IT = 'Information Technology'
    
# Create your models here.
class StaffUser(AbstractUser):
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=20)
    gender = models.CharField(choices=(('Male', 'Male'),('Female', 'Female')), max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table ='staff_user'
        
class Office(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True, unique=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'office'
        
    def __str__(self) -> str:
        return self.name
        
class Section(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=150)
    office = models.ForeignKey(Office, related_name='sections', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table ='section'
    def __str__(self) -> str:
        return self.name
    
class Roles(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True, unique=True)
    user = models.ForeignKey(StaffUser, related_name='roles', on_delete=models.CASCADE)
    office = models.ForeignKey(Office, related_name='roles', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name='roles', on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=50, choices=RoleChoices, default=RoleChoices.STAFF)
    work_role = models.CharField(max_length=50, choices=WorkRoleChoices)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'roles'