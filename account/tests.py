from django.test import TestCase
from .models import Account

class AccountModelTest(TestCase):

    def test_user_creation(self):
        user = Account.objects.create_user(email='testuser@example.com', username='testuser', password='12345')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
