from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(f'users', StaffUserViewset, basename="user")
router.register(f'offices', OfficeViewset, basename="offices")
router.register(f'sections', SectionViewset, basename="sections")
router.register(f'roles', RoleViewset, basename="roles")

urlpatterns = [
    path('', include(router.urls)),
]
