from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from apps.accounts.models import CustomUser, Personalization

class CustomUserCreateSerializer(BaseUserCreateSerializer):
        
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class PersonalizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personalization
        fields = ['id', 'user', 'difficulty', 'personal_details']
        read_only_fields = ['id', 'user']