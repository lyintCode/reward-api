from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя
    Возвращает username, email и coins
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'coins')