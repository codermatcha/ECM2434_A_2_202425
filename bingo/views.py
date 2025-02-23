from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import logging
import os
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Task, UserTask, Leaderboard, BingoTask
from .serializers import TaskSerializer, LeaderboardSerializer, RegisterUserSerializer

User = get_user_model()
logger = logging.getLogger(__name__)

# Task views
class TasksView(APIView):
    """Handles fetching tasks via a class-based API view."""
    
    def get(self, request):
        tasks_data = [
            {'id': 1, 'description': "Finish Green Consultant training", 'points': 10, 'requiresUpload': True},
            {'id': 2, 'description': "Join a 'Green' society", 'points': 7, 'requiresUpload': True},
            {'id': 3, 'description': "Get involved in Gift it, Reuse it scheme", 'points': 10, 'requiresUpload': False},
            {'id': 4, 'description': "Use British Heart Foundation Banks on campus to recycle clothes", 'points': 8, 'requiresUpload': False},
            {'id': 5, 'description': "Sign up to university sustainability newsletter", 'points': 5, 'requiresUpload': True}
        ]
        return Response(tasks_data, status=status.HTTP_200_OK)


# Check user
@api_view(['GET'])
def check_user(request, username):
    """Checks if a user exists by username"""
    user = User.objects.filter(username=username).first()
    if user:
        return Response({"exists": True, "email": user.email})
    return Response({'exists': False, 'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# -------------------------------
# ✅ Email Validation Function
# -------------------------------
def email_validation(email):
    """Ensures email is from University of Exeter"""
    try:
        validate_email(email)
        return email.lower().endswith('@exeter.ac.uk')
    except ValidationError:
        return False

# -------------------------------
# ✅ User Registration API
# -------------------------------
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
def register_user(request):
    """Registers a new user"""
    data = request.data
    username = data.get("username")
    password = data.get("password")
    password_again = data.get("passwordagain")
    email = data.get("email")

    logger.info(f"Incoming registration request: {data}")

    def log_error(error_message, status_code):
        logger.error(f"Registration error: {error_message}")
        return Response({"error": error_message}, status=status_code)

    # ✅ Validate required fields
    if not username or not password or not password_again or not email:
        return log_error("All fields are required.", status.HTTP_400_BAD_REQUEST)

    # ✅ Enforce `@exeter.ac.uk` email requirement
    if not email_validation(email):
        return log_error("Please use your @exeter.ac.uk email only.", status.HTTP_400_BAD_REQUEST)

    # ✅ Ensure username and email are unique
    if User.objects.filter(username=username).exists():
        return log_error("Username already taken.", status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return log_error("This email is already registered.", status.HTTP_400_BAD_REQUEST)

    # ✅ Validate password strength
    try:
        validate_password(password)
    except ValidationError as e:
        return log_error(f"Weak password: {' '.join(e.messages)}", status.HTTP_400_BAD_REQUEST)

    # ✅ Ensure passwords match
    if password != password_again:
        return log_error("Passwords do not match.", status.HTTP_400_BAD_REQUEST)

    # ✅ Create user
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        logger.info(f"User {username} created successfully.")
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return Response({"error": "User registration failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# -------------------------------
# ✅ User Login API
# -------------------------------
@api_view(['POST'])
def login_user(request):
    """Authenticates a user and returns JWT tokens"""
    data = request.data
    username = data.get('username')
    password = data.get('password')

    def log_error(error_message, status_code):
        return Response({"error": error_message}, status=status_code)

    # ✅ Ensure username and password are provided
    if not username or not password:
        return log_error("Username and password are required.", status.HTTP_400_BAD_REQUEST)

    # ✅ Authenticate user
    user = authenticate(username=username, password=password)

    if user is None:
        return log_error("Invalid username or password.", status.HTTP_401_UNAUTHORIZED)

    # ✅ Generate JWT token
    refresh = RefreshToken.for_user(user)
    
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": username
    }, status=status.HTTP_200_OK)

# -------------------------------
# ✅ User Profile API
# -------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Fetches user profile details"""
    user = request.user
    completed_tasks = BingoTask.objects.filter(completed_by=user).count()
    total_points = sum(task.points for task in BingoTask.objects.filter(completed_by=user))

    # Ensure leaderboard exists
    leaderboard, _ = Leaderboard.objects.get_or_create(user=user)

    return Response({
        "username": user.username,
        "total_points": leaderboard.points,
        "completed_tasks": completed_tasks,
        "leaderboard_rank": user_rank(leaderboard.points)
    })

# -------------------------------
# ✅ User Ranking Helper Function
# -------------------------------
def user_rank(points):
    if points < 50:
        return "Beginner"
    elif points > 1250:
        return "Expert"
    return "Intermediate"

# -------------------------------
# ✅ Leaderboard API
# -------------------------------
@api_view(['GET'])
def leaderboard(request):
    players = Leaderboard.objects.order_by('-points')[:10]
    serializer = LeaderboardSerializer(players, many=True)
    return Response(serializer.data)

# -------------------------------
# ✅ Tasks API
# -------------------------------
@api_view(['GET'])
def tasks(request):
    """Returns available tasks"""
    tasks_list = [
        {"id": 1, "description": "Finish Green Consultant training", "points": 10, "requiresUpload": True},
        {"id": 2, "description": "Join a 'Green' society", "points": 7, "requiresUpload": True},
        {"id": 3, "description": "Get involved in Gift it, Reuse it scheme", "points": 10, "requiresUpload": False},
        {"id": 4, "description": "Use British Heart Foundation Banks on campus to recycle clothes", "points": 8, "requiresUpload": False},
        {"id": 5, "description": "Sign up to university sustainability newsletter", "points": 5, "requiresUpload": True}
    ]
    return Response(tasks_list)
