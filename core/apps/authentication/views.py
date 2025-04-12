from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserRegistrationSerializer

class UserRegistrationView(APIView):
    """
    Эндпоинт: POST /api/registration/
    Регистрация нового пользователя
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя",
        request_body=UserRegistrationSerializer,
        responses={
            201: "Пользователь успешно зарегистрирован.",
            400: "Неверные данные."
        }
    )

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Пользователь успешно зарегистрирован."}, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
