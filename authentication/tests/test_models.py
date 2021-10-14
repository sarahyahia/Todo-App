from django.test import TestCase
from authentication.models import User
from utils.setup_tests import TestSetup



class TestModel(TestSetup):
    
    def test_should_create_user(self):
        user = self.create_test_user()
        self.assertEqual(str(user), user.email) # testing email because it's in __str__ function in User Model