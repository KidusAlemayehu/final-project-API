from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from random import choice
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, force_bytes, DjangoUnicodeDecodeError
from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.core.mail import send_mail
from apps.staff_auth.email_templates import EmailTemplates
import string


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize StaffUser model.
    """
    class Meta:
        model = get_user_model()
        fields = ['id', 
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'office',
                  'role',
                  'gender',
                  'is_active',
                  'created_at',
                  'updated_at']
        
    def validate(self, attrs):
        if get_user_model().objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already exists")
        if self.initial_data['office'] == 'HOD' and self.initial_data['role'] != 'Administrator':
            raise serializers.ValidationError("HOD user role  must be set to an Administrator")
        elif self.initial_data['office'] in ['UG', 'PG', 'TA'] and self.initial_data['role'] not in ['Staff', 'Coordinator']:
            raise serializers.ValidationError('For offices UG, PG and TA the roles must be either Staff or Coordinator')
        else:
            pass
        return attrs
    
    def create(self, validated_data):
        default_password = ''.join([choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(8)])
        validated_data['password'] = default_password
        email = validated_data['email']
        sender_email = settings.DEFAULT_FROM_EMAIL
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        uidb64 = urlsafe_b64encode(force_bytes(user.pk))
        token=PasswordResetTokenGenerator().make_token(user)
        password_reset_url= "http://localhost:3000/set_password/?uidb64="+ uidb64.decode()+"&token=" + str(token)
        subject = EmailTemplates.ACCOUNT_CREATED_EMAIL_SUBJECT_TEXT.format("CIT Staff Portal")
        message = EmailTemplates.ACCOUNT_CREATED_EMAIL_MESSAGE_TEXT.format(validated_data['first_name'], "CIT Staff Portal", validated_data['office'], validated_data['role'], password_reset_url, "Username: " +validated_data['username']+"\nTemporary password: "+default_password)
        send_mail(subject, message, sender_email, [email], fail_silently=False)
        return user
    
    