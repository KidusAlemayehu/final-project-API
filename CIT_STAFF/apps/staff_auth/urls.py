from django.urls import path, include
from .views import LoginAPIView, LogoutAPIView, SetChangePasswordView, ChangePasswordView
from rest_framework_simplejwt.views import TokenBlacklistView
urlpatterns = [
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('set_password/', SetChangePasswordView.as_view(), name='password-set'),
]
