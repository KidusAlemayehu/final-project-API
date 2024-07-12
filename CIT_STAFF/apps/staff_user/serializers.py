from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from random import choice
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from base64 import urlsafe_b64encode
from django.core.mail import send_mail
from apps.staff_auth.email_templates import EmailTemplates
from apps.staff_user.models import *
import string

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = '__all__'  

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'  

class RoleSerializer(serializers.ModelSerializer):
    office = serializers.CharField()
    section = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Roles
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }

    def create(self, validated_data):
        office_name = validated_data.pop('office')
        section_name = validated_data.pop('section', None)
        
        office = Office.objects.get(name=office_name)
        validated_data['office'] = office

        if section_name:
            section = Section.objects.get(name=section_name)
            validated_data['section'] = section
        else:
            validated_data['section'] = None

        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'id', 
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'gender',
            'is_active',
            'created_at',
            'updated_at',
            'roles'
        ]
        
    def validate(self, attrs):
        # if get_user_model().objects.filter(email=attrs['email']).exists():
        #     raise serializers.ValidationError("Email already exists")
        if 'roles' in self.initial_data:
            for role in self.initial_data['roles']:
                if role['office'] == 'HOD' and role['role'] != 'Administrator':
                    raise serializers.ValidationError("HOD user role must be set to Administrator")
                elif role['office'] in ['Under Graduate', 'Post Graduate'] and role['role'] not in ['Staff', 'Coordinator']:
                    raise serializers.ValidationError('For offices UG and PG, the roles must be either Staff or Coordinator')
        return attrs
    
    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])
        default_password = ''.join([choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(8)])
        validated_data['password'] = default_password
        email = validated_data['email']
        sender_email = settings.DEFAULT_FROM_EMAIL

        # Create user
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # Create associated roles
        for role_data in roles_data:
            role_data['user'] = user
            RoleSerializer().create(role_data)

        # Send email
        uidb64 = urlsafe_b64encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        password_reset_url = f"http://localhost:3000/set_password/?uidb64={uidb64.decode()}&token={token}"
        subject = EmailTemplates.ACCOUNT_CREATED_EMAIL_SUBJECT_TEXT.format("CIT Staff Portal")
        message = EmailTemplates.ACCOUNT_CREATED_EMAIL_MESSAGE_TEXT.format(
            validated_data['first_name'], 
            "CIT Staff Portal", 
            roles_data[0]['office'], 
            roles_data[0]['role'], 
            password_reset_url, 
            f"Username: {validated_data['username']}\nTemporary password: {default_password}"
        )
        try:
            send_mail(subject, message, sender_email, [email], fail_silently=False)
        except Exception as e:
            print(e)

        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['roles'] = RoleSerializer(instance.roles.all(), many=True).data
        return representation
