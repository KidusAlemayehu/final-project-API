from rest_framework import serializers
from .models import *

class NestedParentSerializer:
    def validate(self, data):
        data['project'] = self.context.get('project')
        print("validating ", data['project'])
        return data
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        validated_data['owner'] = self.context.get('owner')
        project = Project.objects.create(**validated_data)
        project.save()
        project_access_table = ProjectAccessTable.objects.create(project=project)
        project_access_table.save()
        project_acces_role_table = ProjectAccessRoleTable.objects.create(project_access_table=project_access_table, user=self.context.get('owner'), access_role='Owner')
        project_acces_role_table.save()
        return project
        
        
class ProjectTaskSerializer(NestedParentSerializer, serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = '__all__'
        read_only_fields = ['project', 'created_at', 'updated_at']
        
class ProjectAccessTableSerializer(NestedParentSerializer, serializers.ModelSerializer):
    class Meta:
        model = ProjectAccessTable
        fields = '__all__'
        read_only_fields = ['project', 'created_at', 'updated_at']
        
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
        