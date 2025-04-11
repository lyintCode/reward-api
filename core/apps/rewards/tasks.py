from celery import shared_task
from django.utils import timezone

from rewards.models import ScheduledReward, RewardLog

@shared_task
def process_scheduled_rewards() -> None:
    """Обрабатывает запланированные награды"""
    now = timezone.now()
        
    # Получаем все запланированные награды, время которых наступило
    # Ограничение не более 1000 задач за раз
    rewards_to_process = ScheduledReward.objects.filter(execute_at__lte=now)[:1000]
    
    for reward in rewards_to_process:
        # Начисляем coins пользователю
        reward.user.coins += reward.amount
        reward.user.save()
        
        # Создаем запись в RewardLog
        RewardLog.objects.create(
            user=reward.user,
            amount=reward.amount,
            given_at=now
        )
        
        # Удаляем выполненную задачу
        reward.delete()