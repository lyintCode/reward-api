from django.db import models
from django.conf import settings

class ScheduledReward(models.Model):
    """Модель запланированных заданий"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scheduled_rewards'
    )
    amount = models.IntegerField()
    execute_at = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} монет в {self.execute_at}"
    
class RewardLog(models.Model):
    """Модель выполненных заданий"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reward_logs'
    )
    amount = models.IntegerField()
    given_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} монет в {self.given_at}"