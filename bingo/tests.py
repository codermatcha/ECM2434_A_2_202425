from django.test import TestCase
from django.core.exceptions import ValidationError
from .views import email_validation

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
