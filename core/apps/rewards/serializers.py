from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import RewardLog

User = get_user_model()

class RewardLogSerializer(serializers.ModelSerializer):
    """
    Сериализатор для записей RewardLog.
    Возвращает amount и given_at для текущего пользователя.
    """
    class Meta:
        model = RewardLog
        fields = ('amount', 'given_at')

class RewardRequestSerializer(serializers.Serializer):
    """
    Сериализатор для обработки POST /api/rewards/request/.
    Пользователь может запросить награду только один раз в сутки.
    """
    def validate(self, data):
        user = self.context['request'].user

        # Проверяем, прошли ли сутки с момента последнего запроса
        if user.last_reward_request:
            now = timezone.now()
            time_since_last_request = now - user.last_reward_request
            if time_since_last_request.total_seconds() < 86400:  # 1 день
                raise serializers.ValidationError("Вы уже запросили награду сегодня. Попробуйте завтра.")

        return data