from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import RewardLog
from .serializers import RewardLogSerializer

class RewardLogListView(APIView):
    """
    Эндпоинт GET /api/rewards/.
    Доступен только авторизованным пользователям.
    Возвращает список всех записей RewardLog для текущего пользователя.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Получаем текущего пользователя
        user = request.user

        # Фильтруем записи для текущего пользователя
        reward_logs = RewardLog.objects.filter(user=user)

        # Сериализуем данные
        serializer = RewardLogSerializer(reward_logs, many=True)

        # Возвращаем данные в JSON-формате
        return Response(serializer.data, status=status.HTTP_200_OK)