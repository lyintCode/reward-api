from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class UsersTests(APITestCase):
    def setUp(self):
        """Создание пользователя для тестов"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword123",
            coins=500  # Устанавливаем начальное количество монет
        )

        # Получение JWT-токена для пользователя
        token_url = reverse('token_obtain_pair')
        data = {
            "username": "testuser",
            "password": "securepassword123"
        }
        response = self.client.post(token_url, data, format='json')
        self.access_token = response.data["access"]

    def test_get_user_profile(self):
        """Тест получения профиля пользователя"""

        url = reverse('user-profile')

        # Добавляем JWT-токен в заголовки запроса
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["coins"], 500)

    def test_get_user_profile_unauthorized(self):
        """Тест попытки получить профиль без аутентификации"""

        url = reverse('user-profile')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
