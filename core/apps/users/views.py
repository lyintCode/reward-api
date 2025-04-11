from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import UserProfileSerializer

class UserProfileView(APIView):
    """
    Эндпоинт GET /api/profile/.
    Доступен только авторизованным пользователям.
    Возвращает данные: username, email, coins
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Текущий пользователь
        user = request.user

        # Сериализуем данные пользователя
        serializer = UserProfileSerializer(user)

        # Возвращаем данные в JSON-формате
        return Response(serializer.data, status=status.HTTP_200_OK)