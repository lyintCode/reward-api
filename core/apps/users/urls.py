from django.urls import path

from .views import UserProfileView, UserRegistrationView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('registration/', UserRegistrationView.as_view(), name='user-registration'),
]