from django.urls import path
from .views import get_tasks, complete_task, leaderboard, register_user, login_user, get_user_data
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('tasks/', get_tasks, name='tasks'),
    path('complete_task/', complete_task, name='complete_task'),
    path('leaderboard/', leaderboard, name='leaderboard'),

    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('user/', get_user_data, name='user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
