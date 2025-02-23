from django.test import TestCase
from django.core.exceptions import ValidationError
from .views import email_validation

class EmailValidationTest(TestCase):
    def assertEmailValidation(self, email, expected_result, msg):
        """Helper method to test email validation."""
        result = email_validation(email)
        self.assertEqual(result, expected_result, msg)

# Create your tests here.
