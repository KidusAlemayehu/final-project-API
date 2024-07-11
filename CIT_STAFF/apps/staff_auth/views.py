from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from apps.staff_user.serializers import UserSerializer
from django.contrib.auth import get_user_model
from .token import token_expire_handler, expires_in, is_token_expired
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from apps.staff_auth import permission_handler as MyPermissions
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from apps.staff_user.serializers import UserSerializer


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
        
class GetCurrentUserView(APIView):
    serializer_class = UserSerializer
    permission_classes = [MyPermissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.filter(pk=request.user.pk).first()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [MyPermissions.IsAuthenticated]
    
    def get(self, request):
         if request.user.is_authenticated:
            uidb64 = urlsafe_b64encode(force_bytes(request.user.pk))
            token = PasswordResetTokenGenerator().make_token(request.user)
            relative_uri = "http://localhost:3000/set_password/"+"?uidb64=" + uidb64.decode() + "&token=" + str(token)
            change_link =  relative_uri
            data = {'change_password_link': change_link}
            return Response(data, status=status.HTTP_200_OK)
     
class SetChangePasswordView(APIView):
    queryset = get_user_model().objects.all()
    
    def put(self, request, format='json'):
        """
        Allows resetting password using a unique link 
        """
        uidb64 = request.GET.get('uidb64')
        token = request.GET.get('token')
        user_model = get_user_model()

        new_password = request.data.get("password")
        confirm_password = request.data.get("confirmPassword")
        
        if new_password and confirm_password:
            if new_password!= confirm_password:
                raise ValidationError("Passwords don't match", code='authorization')
        else:
            raise ValidationError('Must include "password" and "confirm_password".', code='authorization')
        
        token_generator = PasswordResetTokenGenerator()
        try:
            uid = urlsafe_b64decode(uidb64).decode('utf-8')
            print("UID: %s" % uid)
            user = user_model.objects.get(pk=uid)
        except(ValueError, OverflowError, user_model.DoesNotExist):
            user = None
        print("USER: %s" % user)
        if user:
            if token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'success': 'Password was successfully Changed'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Request. Token may have expired.'}, status=status.HTTP_401_UNAUTHORIZED) 
        else:
            return Response({'error': 'Invalid Request. Unable to parse data'}, status=status.HTTP_400_BAD_REQUEST)
        