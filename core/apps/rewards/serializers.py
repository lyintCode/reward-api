from rest_framework import serializers
from .models import RewardLog

class RewardLogSerializer(serializers.ModelSerializer):
    """
    Сериализатор для записей RewardLog.
    Возвращает amount и given_at для текущего пользователя.
    """
    class Meta:
        model = RewardLog
        fields = ('amount', 'given_at')