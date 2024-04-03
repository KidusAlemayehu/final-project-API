from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=20, write_only=True)
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
                  'password',
                  'confirm_password',
                  'gender',
                  'is_active',
                  'created_at',
                  'updated_at']
        extra_kwargs = {'password': {'write_only': True},
                        'confirm_password': {'write_only': True}}
        
    def validate(self, attrs):
        if self.initial_data['office'] == 'HOD' and self.initial_data['role'] != 'Administrator':
            raise serializers.ValidationError("HOD user role  must be set to an Administrator")
        elif self.initial_data['office'] in ['UG', 'PG', 'TA'] and self.initial_data['role'] not in ['Staff', 'Coordinator']:
            raise serializers.ValidationError('For offices UG, PG and TA the roles must be either Staff or Coordinator')
        else:
            pass
        return attrs
    
    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        password = validated_data['password']
        
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError('Password mismatch!')
        
        user = get_user_model().objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    