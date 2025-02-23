from django.test import TestCase

from django.core.exceptions import ValidationError
from .views import email_validation, user_rank, leaderboard, tasks
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
User = get_user_model()


class EmailValidationTest(TestCase):
    def assertEmailValidation(self, email, expected_result, msg):
        """Helper method to test email validation."""
        result = email_validation(email)
        self.assertEqual(result, expected_result, msg)

    def test_valid_exeter_email(self):
        """Emails with a valid Exeter domain should return True."""
        self.assertEmailValidation("test@exeter.ac.uk", True, "Valid Exeter email should return True")
        self.assertEmailValidation("TEST@EXETER.AC.UK", True, "Uppercase Exeter email should return True")

    def test_invalid_email_domains(self):
        """Non-Exeter domains should return False."""
        self.assertEmailValidation("test@example.com", False, "Non-Exeter email should return False")
        self.assertEmailValidation("test@exeteracuk", False, "Email missing dot should return False")
        self.assertEmailValidation("test@exetr.ac.uk", False, "Email with missing letter in domain should return False")
        self.assertEmailValidation("test@exeter.ac .uk", False, "Email with extra space should return False")

    def test_invalid_email_formats(self):
        """Incorrectly formatted emails should return False."""
        self.assertEmailValidation("testexeter.ac.uk", False, "Incorrectly formatted email should return False")
        self.assertEmailValidation("", False, "Empty string email should return False")
        self.assertEmailValidation(None, False, "Null email input should return False")

class RegisterUserTests(TestCase):
    def setUp(self):
        """Set up the test client and user registration URL."""
        self.client = APIClient()
        self.registration_url = reverse('register_user')  # Ensure you have named your URL in urls.py
        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@exeter.ac.uk',
            'password': 'validPassword123!',
            'passwordagain': 'validPassword123!'
        }

    def test_register_user_success(self):
        """Test successful registration."""
        response = self.client.post(self.registration_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

    def test_register_user_missing_fields(self):
        """Test registration failure due to missing fields."""
        for key in self.user_data.keys():
            data = {k: v for k, v in self.user_data.items() if k != key}
            response = self.client.post(self.registration_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('error', response.data)

    def test_register_user_invalid_email(self):
        """Test registration with an invalid email."""
        data = self.user_data.copy()
        data['email'] = 'invalidemail'
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_register_user_existing_username(self):
        """Test registration with an already existing username."""
        User.objects.create_user(username='newuser', email='other@exeter.ac.uk', password='password123')
        response = self.client.post(self.registration_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_register_user_existing_email(self):
        """Test registration with an already existing email."""
        User.objects.create_user(username='otheruser', email='newuser@exeter.ac.uk', password='password123')
        response = self.client.post(self.registration_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_register_user_weak_password(self):
        """Test registration with a weak password."""
        data = self.user_data.copy()
        data['password'] = '123'
        data['passwordagain'] = '123'
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_register_user_password_mismatch(self):
        """Test registration failure when passwords do not match."""
        data = self.user_data.copy()
        data['passwordagain'] = 'differentPassword123!'
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

class LoginUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        self.login_url = reverse('login_user')

    def test_login_user_success(self):
        """Test logging in with correct credentials."""
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Assuming JWT returns access token key

    def test_login_user_incorrect_password(self):
        """Test logging in with incorrect password."""
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_user_nonexistent(self):
        """Test logging in with a username that does not exist."""
        data = {'username': 'nouser', 'password': 'password123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_user_inactive(self):
        """Test logging in with an inactive user."""
        self.user.is_active = False
        self.user.save()
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='user@example.com', password='testpass123')
        self.profile_url = reverse('user_profile')

    def test_get_user_profile_authenticated(self):
        """Test retrieving a user profile for a logged-in user."""
        self.client.force_authenticate(user=self.user)  # Force authentication of the user
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], self.user.username)

    def test_get_user_profile_unauthenticated(self):
        """Test retrieving a user profile without being logged in."""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserRankTests(TestCase):
    def test_user_rank_beginner(self):
        """Test that users with less than 50 points are ranked as 'Beginner'."""
        self.assertEqual(user_rank(0), 'Beginner')
        self.assertEqual(user_rank(25), 'Beginner')
        self.assertEqual(user_rank(49), 'Beginner')

    def test_user_rank_intermediate(self):
        """Test that users with 50 to 1250 points are ranked as 'Intermediate'."""
        self.assertEqual(user_rank(50), 'Intermediate')
        self.assertEqual(user_rank(625), 'Intermediate')
        self.assertEqual(user_rank(1250), 'Intermediate')

    def test_user_rank_expert(self):
        """Test that users with more than 1250 points are ranked as 'Expert'."""
        self.assertEqual(user_rank(1251), 'Expert')
        self.assertEqual(user_rank(2500), 'Expert')

class LeaderboardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.leaderboard_url = reverse('leaderboard')  # Update URL name
        # Create several users
        users = [
            {'username': 'user1', 'points': 150},
            {'username': 'user2', 'points': 250},
            {'username': 'user3', 'points': 50},
            {'username': 'user4', 'points': 350},
            {'username': 'user5', 'points': 450}
        ]
        for user in users:
            usr = User.objects.create_user(username=user['username'], password='testpass123')
            leaderboard.objects.create(user=usr, points=user['points'])

    def test_leaderboard_order(self):
        """Test that the leaderboard is returned in descending order of points."""
        response = self.client.get(self.leaderboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data is ordered correctly
        last_points = float('inf')
        for entry in response.data:
            self.assertLessEqual(entry['points'], last_points)
            last_points = entry['points']

    def test_leaderboard_entries(self):
        """Test that the leaderboard has the correct number of entries."""
        response = self.client.get(self.leaderboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)  # Expect 5 entries as created in setUp

    def test_leaderboard_content(self):
        """Test the content of the leaderboard entries."""
        response = self.client.get(self.leaderboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_users = ['user5', 'user4', 'user2', 'user1', 'user3']  # Sorted by points
        actual_users = [entry['username'] for entry in response.data]
        self.assertEqual(actual_users, expected_users)

class TasksViewTests(TestCase):
    def test_tasks_view(self):
        """
        Test the tasks function to ensure it returns the correct task list as JSON.
        """
        response = self.client.get(reverse('tasks'))  # Update Url name
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Load the response data
        tasks_list = response.json()

        # Define what you expect to receive
        expected_tasks_list = [
            {"id": 1, "description": "Finish Green Consultant training", "points": 10, "requiresUpload": True,
             "requireScan": False},
            {"id": 2, "description": "Join a 'Green' society", "points": 7, "requiresUpload": True,
             "requireScan": False},
            {"id": 3, "description": "Get involved in Gift it, Reuse it scheme", "points": 10, "requiresUpload": False,
             "requireScan": True},
            {"id": 4, "description": "Use British Heart Foundation Banks on campus to recycle clothes", "points": 8,
             "requiresUpload": False, "requireScan": True},
            {"id": 5, "description": "Sign up to university sustainability newsletter", "points": 5,
             "requiresUpload": True, "requireScan": False},
        ]

        # Check if the returned list matches the expected list
        self.assertEqual(tasks_list, expected_tasks_list)

class CheckUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.existing_user = User.objects.create_user(username='testuser', email='user@example.com', password='testpass123')
        self.check_user_url = lambda username: reverse('check_user', kwargs={'username': username}) #Update Url name

    def test_check_user_exists(self):
        """Test checking a user that does exist."""
        url = self.check_user_url(self.existing_user.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['exists'])
        self.assertEqual(response.data['email'], self.existing_user.email)

    def test_check_user_does_not_exist(self):
        """Test checking a user that does not exist."""
        url = self.check_user_url('nonexistentuser')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['exists'])
        self.assertEqual(response.data['error'], 'User not found')

#LeaderboardTests, TasksViewTests, CheckUserTests. Error due to lack of url name