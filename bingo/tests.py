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
