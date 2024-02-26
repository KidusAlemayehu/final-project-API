from django.urls import path, include
from .views import LoginAPIView, LogoutAPIView
from rest_framework_simplejwt.views import TokenBlacklistView
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
