from django.contrib import admin
from .models import ScheduledReward, RewardLog

@admin.register(ScheduledReward)
class ScheduledRewardAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'execute_at')
    search_fields = ('user__username',)
    list_filter = ('execute_at',)

@admin.register(RewardLog)
class RewardLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'given_at')
    search_fields = ('user__username',)
    list_filter = ('given_at',)