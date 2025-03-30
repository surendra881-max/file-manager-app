from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UploadedFile

# ✅ SAFE User Serializer (only returns username, avoids recursion)
class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# ✅ Uploaded File Serializer using UserDisplaySerializer to prevent recursion
class UploadedFileSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)

    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_at', 'file_type', 'user']


# ✅ User Registration Serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )


# ✅ Username Update Serializer
class UsernameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
from .models import UserProfile, Address

# 🔹 Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_line', 'city', 'state', 'postal_code', 'country']

# 🔹 UserProfile Serializer (phone number + nested addresses)
class UserProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'addresses']

# 🔹 Phone number update only
class PhoneUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number']

# 🔹 Create / Update address serializer
class AddressCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_line', 'city', 'state', 'postal_code', 'country']
