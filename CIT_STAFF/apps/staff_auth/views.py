from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from apps.staff_user.serializers import UserSerializer
from django.contrib.auth import get_user_model
from .token import token_expire_handler, expires_in, is_token_expired
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout


# Create your views here.
class LoginAPIView(APIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """
    serializer_class = LoginSerializer
    
    @csrf_exempt
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        serializer = UserSerializer(user)
        token, _ = Token.objects.get_or_create(user=user)
        is_expired, token = token_expire_handler(token)
        login(request, user)
        data = serializer.data
        data["token"] = {"key": token.key, "expires in": expires_in(token)}
        return Response(data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print("request user is", request.user)
            request.user.auth_token.delete()
            logout(request)
            return Response({"message":"logout successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"user is not authenticated"}, status=status.HTTP_403_FORBIDDEN)
        
        