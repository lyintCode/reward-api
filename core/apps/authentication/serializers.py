from typing import Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as DjangoUser # Для типизации
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя"""
    
    # Описание типа полей
    username = serializers.CharField(
        max_length=150,
        help_text="Имя пользователя",
    )
    email = serializers.EmailField(
        help_text="Адрес электронной почты",
    )
    password = serializers.CharField(
        write_only=True,
        help_text="Пароль пользователя",
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, value: str) -> str:
        """
        Проверяет уникальность usaername
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует")
        return value

    def validate_email(self, value: str) -> str:
        """
        Проверяет уникальность email
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def create(self, validated_data: Dict[str, str]) -> DjangoUser:
        """ Создание нового польщзователя """

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user