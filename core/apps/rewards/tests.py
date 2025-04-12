from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from rewards.models import RewardLog, ScheduledReward

class RewardsTests(APITestCase):
    def setUp(self):
        """Создание пользователя и начальных данных для тестов"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        self.client.force_authenticate(user=self.user)

        # Создаем запись о предыдущем запросе награды
        self.reward_log = RewardLog.objects.create(
            user=self.user,
            amount=100
        )

    def test_reward_log_list(self):
        """Тест получения списка наград для текущего пользователя"""

        url = reverse('reward-log-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Должна быть одна запись

        reward_data = response.data[0]
        self.assertEqual(reward_data["amount"], 100)
        self.assertIn("given_at", reward_data)  # Проверяем поле given_at

    def test_reward_request_success(self):
        """Тест успешного запроса награды после истечения суток"""

        # Обновляем время последнего запроса на более чем сутки назад
        self.user.last_reward_request = timezone.now() - timedelta(days=2)
        self.user.save()

        url = reverse('reward-request')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("status", response.data)
        self.assertEqual(
            response.data["status"],
            "Награда успешно запрошена. Она будет начислена через 5 минут."
        )

        # Проверяем, что новая запись создана в ScheduledReward
        self.assertEqual(ScheduledReward.objects.filter(user=self.user).count(), 1)

    def test_reward_request_same_day(self):
        """Тест попытки запросить награду дважды за один день"""

        # Устанавливаем время последнего запроса на текущее время
        self.user.last_reward_request = timezone.now()
        self.user.save()

        url = reverse('reward-request')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Вы уже запросили награду сегодня. Попробуйте завтра."
        )

        # Проверяем, что новых записей не создано
        self.assertEqual(ScheduledReward.objects.filter(user=self.user).count(), 0)

    def test_reward_log_list_unauthorized(self):
        """Тест попытки получить список наград без аутентификации"""

        self.client.logout()

        url = reverse('reward-log-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reward_request_unauthorized(self):
        """Тест попытки запросить награду без аутентификации"""

        self.client.logout()

        url = reverse('reward-request')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)