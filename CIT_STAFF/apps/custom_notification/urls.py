from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserNotificationsView

router = DefaultRouter()
router.register(r'notifications', UserNotificationsView, basename='notifications')

urlpatterns = [
    path('', include(router.urls))
]
