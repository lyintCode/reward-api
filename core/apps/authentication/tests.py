from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User

class AuthenticationTests(APITestCase):
    
    def setUp(self):
        """Создание пользователя для тестов"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )

    def test_user_registration(self):
        """Тест регистрации пользователя"""

        url = reverse('user-registration')

        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword123"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Пользователь успешно зарегистрирован.")

    def test_invalid_registration(self):
        """Тест попытки регистрации с уже существующим username и email"""

        url = reverse('user-registration')
        
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        }
        # Первый запрос успешен
        self.client.post(url, data, format='json')

        # Должна быть ошиька, ведь пользователь существует
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

    def test_token_obtain_pair(self):
        """Тест получения пары токенов (access и refresh)"""

        url = reverse('token_obtain_pair')

        data = {
            "username": "testuser",
            "password": "securepassword123"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_obtain_pair_invalid_credentials(self):
        """Тест попытки получения токенов с неверными учетками"""

        url = reverse('token_obtain_pair')

        data = {
            "username": "wronguser",
            "password": "wrongpassword"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Не найдено активной учетной записи с указанными данными")

    def test_token_refresh(self):
        """Тест обновления access-токена по refresh-токену"""

        # Сначала получаем refresh-токен
        token_url = reverse('token_obtain_pair')
        data = {
            "username": "testuser",
            "password": "securepassword123"
        }
        response = self.client.post(token_url, data, format='json')
        refresh_token = response.data["refresh"]

        url = reverse('token_refresh')

        data = {
            "refresh": refresh_token
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_refresh_invalid_token(self):
        """Тест попытки обновления токена с неверным refresh-токеном"""

        url = reverse('token_refresh')

        data = {
            "refresh": "invalid-refresh-token"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["code"], "token_not_valid")

    def test_token_verify(self):
        """Тест верификации access-токена"""

        # Сначала получаем access-токен
        token_url = reverse('token_obtain_pair')
        data = {
            "username": "testuser",
            "password": "securepassword123"
        }
        response = self.client.post(token_url, data, format='json')
        access_token = response.data["access"]

        url = reverse('token_verify')

        data = {
            "token": access_token
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_verify_invalid_token(self):
        """Тест попытки верификации неверного access-токена"""

        url = reverse('token_verify')

        data = {
            "token": "invalid-access-token"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["code"], "token_not_valid")