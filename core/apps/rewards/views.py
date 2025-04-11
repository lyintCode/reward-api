from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import ScheduledReward, RewardLog
from .serializers import RewardLogSerializer, RewardRequestSerializer

class RewardLogListView(APIView):
    """
    Эндпоинт: GET /api/rewards/
    Доступен только авторизованным пользователям
    Возвращает список всех записей RewardLog для текущего пользователя
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список наград текущего пользователя",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT Token. Пример: Bearer [token]",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: RewardLogSerializer(many=True),
            401: "Учетные данные не были предоставлены."
        }
    )

    def get(self, request: Request, *args, **kwargs) -> Response:
        # Получаем текущего пользователя
        user = request.user

        # Фильтруем записи для текущего пользователя
        reward_logs = RewardLog.objects.filter(user=user)

        # Сериализуем данные
        serializer = RewardLogSerializer(reward_logs, many=True)

        # Возвращаем данные в JSON-формате
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RewardRequestView(APIView):
    """
    Эндпоинт: POST /api/rewards/request/
    Ппользователь может запросить награду только один раз в сутки
    Создает ScheduledReward с временем выполнения через 5 минут
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Запросить награду",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="JWT Token. Пример: Bearer [token]",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            201: "Награда успешно запрошена. Она будет начислена через 5 минут.",
            400: "Вы уже запросили награду сегодня. Попробуйте завтра."
        }
    )

    def post(self, request: Request, *args, **kwargs) -> Response:
        # Валидация данных
        serializer = RewardRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Dыполнениt награды через 5 минут
        execute_at = timezone.now() + timezone.timedelta(minutes=5)

        # Создаем ScheduledReward
        ScheduledReward.objects.create(
            user=user,
            amount=100,
            execute_at=execute_at
        )

        # Обновляем поле last_reward_request у пользователя
        user.last_reward_request = timezone.now()
        user.save()

        return Response(
            {"status": "Награда успешно запрошена. Она будет начислена через 5 минут."}, 
            status=status.HTTP_201_CREATED
        )