from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from .views import *

router = DefaultRouter()
router.register(r'project', ProjectViewset, basename='project')

task_nested_router = NestedSimpleRouter(router, r'project', lookup='project')
task_nested_router.register(r'task', ProjectTaskViewset, basename='task')

access_table_nested_router = NestedSimpleRouter(router, r'project', lookup='project')
access_table_nested_router.register(r'access_table', ProjectAccessTableViewset, basename='access_table')

role_table_router = NestedSimpleRouter(access_table_nested_router, r'access_table', lookup='access_table')
role_table_router.register(r'role_table', ProjectAccessRoleTableViewset, basename='role_table')

comment_nested_router = NestedSimpleRouter(task_nested_router, r'task', lookup='task')
comment_nested_router.register(r'comment', ProjectTaskCommentViewset, basename='comment')

assignee_nested_router = NestedSimpleRouter(task_nested_router, r'task', lookup='task')
assignee_nested_router.register(r'assignee', ProjectTaskAssigneeViewset, basename='assignee')

urlpatterns =[
    path('', include(router.urls)),
    path('', include(task_nested_router.urls)),
    path('', include(access_table_nested_router.urls)),
    path('', include(role_table_router.urls)),
    path('', include(comment_nested_router.urls)),
    path('', include(assignee_nested_router.urls)),
]
