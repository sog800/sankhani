from rest_framework import serializers
from .models import CustomUser, UserBusinessProfile



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # Create a new user with the validated data
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class UserBusinessProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # Get username from the user model
    email = serializers.EmailField(source='user.email', read_only=True)  # Get email from the user model

    class Meta:
        model = UserBusinessProfile
        fields = ['is_business', 'business_name', 'phone_number', 'category', 'district', 'username', 'email']
        read_only_fields = ['user']