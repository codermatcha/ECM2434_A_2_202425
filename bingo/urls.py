from django.urls import path
from django.contrib import admin
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

# Remove this admin class as it's not properly configured and not needed in urls.py
# @admin.register
# class CustomAdmin(admin.ModelAdmin):
#     pass

router = DefaultRouter()
router.register(r'challenges', views.ChallengeViewSet)
router.register(r'user-challenges', views.UserChallengeViewSet)
router.register(r'leaderboard', views.LeaderboardViewSet)
router.register(r'rewards', views.RewardViewSet)

urlpatterns = [
    # Authentication
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.login_user, name='login'),
    
    # Game functionality
    path('tasks/', views.tasks, name='tasks'),
    path('complete-task/', views.complete_task, name='complete_task'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('check-user/<str:username>/', views.check_user, name='check_user'),
    path('profile/', views.get_user_profile, name='user_profile'),
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls

