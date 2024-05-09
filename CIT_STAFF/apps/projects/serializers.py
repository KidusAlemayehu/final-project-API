from rest_framework import serializers
from .models import *

class NestedParentSerializer:
    def validate(self, data):
        pass
    
class ProjectTaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTaskComment
        fields = '__all__'
        read_only_fields = ['task', 'created_at', 'updated_at', 'commented_by']
        
    def validate(self, attrs):
        attrs['task'] = self.context.get('project_task')
        attrs['commented_by'] = self.context.get('commented_by')
        return attrs
    
class ProjectTaskSerializer(serializers.ModelSerializer):
    comments = ProjectTaskCommentSerializer(many=True, read_only=True)
    class Meta:
        model = ProjectTask
        fields = ['id', 'name', 'description', 'project', 'task_weight', 'created_at', 'updated_at', 'progress', 'comments']
        read_only_fields = ['project', 'created_at', 'updated_at', 'progress']
        
    def validate(self, attrs):
        attrs['project'] = self.context.get('project')
        return attrs

class ProjectAccessRoleTableSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = ProjectAccessRoleTable
        fields = '__all__'
        read_only_fields = ['project_access_table', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        validated_data['project_access_table'] = self.context.get('project_access_table')
        project_access_role_table = ProjectAccessRoleTable.objects.create(**validated_data)
        project_access_role_table.save()
        return project_access_role_table
        
class ProjectAccessTableSerializer(NestedParentSerializer, serializers.ModelSerializer):
    access_role_table = ProjectAccessRoleTableSerializer(many=True, read_only=True)
    class Meta:
        model = ProjectAccessTable
        fields = ['id', 'project', 'access_role_table']
        read_only_fields = ['project', 'created_at', 'updated_at']
        
    def validate(self, data):
        data['project'] = self.context.get('project')
        if self.Meta.model.objects.filter(project=data['project']).exists():
            return serializers.ValidationError("More than one access table can not be created for one project.")
        return data   
         
class ProjectSerializer(serializers.ModelSerializer):
    tasks = ProjectTaskSerializer(many=True, read_only=True)
    access_table = ProjectAccessTableSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'expected_start_date', 'expected_end_date', 'owner', 'created_at', 'updated_at', 'tasks', 'access_table']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        validated_data['owner'] = self.context.get('owner')
        project = Project.objects.create(**validated_data)
        project.save()
        project_access_table = ProjectAccessTable.objects.create(project=project)
        project_access_table.save()
        project_acces_role_table = ProjectAccessRoleTable.objects.create(project_access_table=project_access_table, user=self.context.get('owner'), access_role='Owner')
        project_acces_role_table.save()
        return project
        
  
class ProjectTaskAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTaskAssignment
        fields = '__all__'
        read_only_fields = ['task', 'created_at', 'updated_at']
        
    def validate(self, attrs):
        attrs['task'] = self.context.get('project_task')
        return attrs
        
    
        