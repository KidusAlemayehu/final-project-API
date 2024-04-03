from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from .views import *

router = DefaultRouter()

router.register(r'project', ProjectViewset, basename='project')
project_nested_router = NestedSimpleRouter(router, r'project', lookup='project')
project_nested_router.register(r'task', ProjectTaskViewset, basename='task')
project_nested_router.register(r'access_table', ProjectAccessTableViewset, basename='access_table')
role_table_router = NestedSimpleRouter(project_nested_router, r'access_table', lookup='access_table')
role_table_router.register(r'role_table', ProjectAccessRoleTableViewset, basename='role_table')

urlpatterns =[
    path('', include(router.urls)),
    path('', include(project_nested_router.urls)),
    path('', include(role_table_router.urls)),
]
