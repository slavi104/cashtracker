from django.test import TestCase
from app_cashtracker.models.User import User
from django.shortcuts import get_object_or_404
from django.utils import timezone


class UserTests(TestCase):

    def test_create_user(self):
        now = timezone.now()
        user = User()
        user.created = now
        user.save()

        self.assertEqual(user, get_object_or_404(User, id=user.id))

    def test_register(self):
        user = User()
        params = {'email': 'test@test.com', 'password_1': 'TESTPASSWORD'}
        user.register(params)

        self.assertEqual(user, get_object_or_404(User, id=user.id))
        self.assertEqual(user.email, 'test@test.com')
        self.assertNotEqual(user.password, 'TESTPASSWORD')

    def test_to_str_for_user(self):
        user = User()
        params = {'email': 'test@test.com', 'password_1': 'TESTPASSWORD'}
        user.register(params)
        user.first_name = 'John'
        user.last_name = 'John'
        user.save()

        self.assertEqual(str(user), user.first_name + ' ' + user.last_name)
