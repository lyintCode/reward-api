from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import UserProfileSerializer

class UserProfileView(APIView):
    """
    Эндпоинт: GET /api/profile/
    Доступен только авторизованным пользователям
    Возвращает данные: username, email, coins
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить профиль текущего пользователя",
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
            200: openapi.Response(
                description="Профиль пользователя успешно получен.",
                schema=UserProfileSerializer
            ),
            401: "Учетные данные не были предоставлены."
        }
    )

    def get(self, request: Request, *args, **kwargs) -> Response:
        user = request.user

        # Сериализуем данные пользователя
        serializer = UserProfileSerializer(user)

        # Возвращаем данные в JSON-формате
        return Response(serializer.data, status=status.HTTP_200_OK)