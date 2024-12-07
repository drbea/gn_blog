from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from accounts.models import User  # Import du modèle

class UserRoleTest(TestCase):
    def test_user_roles(self):
        admin_user = User.objects.create_user(username="admin", password="adminpass", role=User.ADMIN)
        self.assertEqual(admin_user.role, User.ADMIN)
