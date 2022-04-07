from djoser.serializers import UserCreateSerializer
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        return False
    
    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
