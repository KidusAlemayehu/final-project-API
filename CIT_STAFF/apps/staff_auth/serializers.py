from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password, make_password


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=20)
        
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user_model = get_user_model()
            user = user_model.objects.filter(username=username).first()
            if user is not None:
                if not check_password(password, user.password):
                    raise serializers.ValidationError("invalid credentials", code='authorization')
            else:
                raise serializers.ValidationError("User doesn't exist", code='authorization')
        else:
            raise serializers.ValidationError('Must include "username" and "password".', code='authorization')

        data['user'] = user
        return data