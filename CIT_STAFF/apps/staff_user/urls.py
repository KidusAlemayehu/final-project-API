from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(f'users', StaffUserViewset, basename="user")

urlpatterns = [
    path('', include(router.urls)),
]
