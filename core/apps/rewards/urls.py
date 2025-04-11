from django.urls import path
from .views import RewardLogListView

urlpatterns = [
    path('rewards/', RewardLogListView.as_view(), name='reward-log-list'),
]