from django.db import models
from apps.staff_user.models import StaffUser


# Create your models here.
class Project(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True, null=False)
    name = models.CharField(max_length=100, verbose_name="Project Name", blank=False, null=False)
    description = models.TextField(verbose_name="Project Description (Optional)", blank=True, null=True)
    expected_start_date = models.DateField(verbose_name="Expected Start Date", blank=True, null=True)
    expected_end_date = models.DateField(verbose_name="Expected End Date", blank=True, null=True)
    owner = models.ForeignKey(StaffUser, null=True, on_delete=models.SET_NULL, verbose_name="Owner", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'project'
        
    def __str__(self) -> str:
        return self.name
    
class ProjectAccessTable(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Project", blank=False, null=False)
    
    class Meta:
        db_table = 'project_access_table'
    
    
class ACCESS_ROLE_CHOICES(models.TextChoices):
    OWNER = 'Owner'
    CONTRIBUTOR = 'Contributor'
    VIEWER = 'Viewer'
    COMMENTER = 'Commenter'
    
class ProjectAccessRoleTable(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True, null=False)
    project_access_table = models.ForeignKey(ProjectAccessTable, null=False, on_delete=models.CASCADE, verbose_name="Project Access Table", blank=False)
    user = models.ForeignKey(StaffUser, null=False, on_delete=models.CASCADE, verbose_name="Staff User", blank=False)
    access_role = models.CharField(max_length=20, choices=ACCESS_ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'project_access_role_table'
        
class PROJECT_TASK_PROGRESS_CHOICES(models.TextChoices):
    OPEN = 'Open'
    WORKING = 'Working'
    PENDING = 'Pending'
    OVERDUE = 'Overdue'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
        
class ProjectTask(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True, null=False)
    name = models.CharField(max_length=100, verbose_name='Task Name', blank=False, null=False)
    description = models.TextField(verbose_name="Task Description (Optional)", blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Project", blank=False, null=False)
    task_weight = models.FloatField(verbose_name="Task Weight Value", null=True, blank=True)
    progress = models.CharField(max_length=50, choices=PROJECT_TASK_PROGRESS_CHOICES, default=PROJECT_TASK_PROGRESS_CHOICES.OPEN)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'project_task'
        
    def __str__(self) -> str:
        return self.name
    
class ProjectTaskComment(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True, null=False)
    comment = models.TextField(blank=True, max_length=500)
    task = models.ForeignKey(ProjectTask, related_name="commented_on", on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'project_task_comment'
    
class ProjectTaskDependency(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True, null=False)
    task = models.ForeignKey(ProjectTask, on_delete=models.SET_NULL, null=True, blank=True, related_name="base_task")
    depends_on = models.ForeignKey(ProjectTask, on_delete=models.SET_NULL, null=True, blank=True, related_name="depends_on")
    
    class Meta:
        db_table = 'project_task_dependency'
        
class ProjectTaskAssignment(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True, null=False)
    task = models.ForeignKey(ProjectTask, null=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(StaffUser, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'project_task_assignment'
        
def attachment_path(instance, filename):
    return 'Files/Project_{0}/Task_{1}/{2}'.format(instance.task.project.name, instance.task.id, filename)
        
class ProjectTaskAttachment(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True, unique=True, null=False)
    attachment = models.FileField(upload_to=attachment_path)
    task = models.ForeignKey(ProjectTask, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        db_table = 'project_task_attachment'
    
    