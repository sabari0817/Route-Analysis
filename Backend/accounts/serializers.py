from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'travels_name', 'phone_number', 'email', 'place']

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'travels_name', 'phone_number', 'email', 'place', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    login_id = serializers.CharField()  # Can be Email or Phone
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        login_id = data.get('login_id')
        password = data.get('password')

        if not login_id or not password:
            raise serializers.ValidationError("Both 'login_id' and 'password' are required.")

        user = None
        # Check if login_id is an email or phone number
        if '@' in login_id:
            user = User.objects.filter(email=login_id).first()
        else:
            user = User.objects.filter(phone_number=login_id).first()

        if user:
            if user.check_password(password):
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                return user
            else:
                raise serializers.ValidationError("Incorrect password.")
        else:
            raise serializers.ValidationError("Invalid email or phone number.")
