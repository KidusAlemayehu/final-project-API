from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from .views import *


router = DefaultRouter()
router.register(r'event_schedule', EventScheduleViewset, basename='event')

event_invitation_nested_router = NestedSimpleRouter(router, r'event_schedule', lookup='event_schedule')
event_invitation_nested_router.register(r'invitation', EventScheduleInvitation, basename='event_invitation')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(event_invitation_nested_router.urls)),
]
