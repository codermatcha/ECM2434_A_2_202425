from rest_framework import serializers
from django.contrib.auth.models import User  # If using default Django User model
from .models import Task, UserTask, Leaderboard
import logging

logger = logging.getLogger(__name__)

class RegisterUserSerializer(serializers.ModelSerializer):
    passwordagain = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'passwordagain']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """ Ensure only University of Exeter email is used. """
        if not value.lower().endswith('@exeter.ac.uk'):
            raise serializers.ValidationError("Please use your @exeter.ac.uk email only.")
        return value.lower()

    def validate(self, data):
        """ Ensure password and confirmation match. """
        if data['password'] != data['passwordagain']:
            raise serializers.ValidationError({"passwordagain": "Passwords do not match"})
        return data

    def create(self, validated_data):
        """ Create user and initialize their leaderboard entry. """
        validated_data.pop('passwordagain')  # Remove duplicate password field

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Create leaderboard entry (assuming default points = 0)
        Leaderboard.objects.create(user=user, points=0)

        return user
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = '__all__'

class LeaderboardSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Leaderboard
        fields = ['user', 'points']
