from django.urls import path
from .views import RewardLogListView, RewardRequestView

urlpatterns = [
    path('rewards/', RewardLogListView.as_view(), name='reward-log-list'),
    path('rewards/request/', RewardRequestView.as_view(), name='reward-request'),
]