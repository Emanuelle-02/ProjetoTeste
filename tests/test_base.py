from django.test import TestCase
from usuario.models import User

class TestSetup(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def create_test_user(self):
        user = User.objects.create_user(username='teste101', email='teste101@gmail.com')
        user.set_password('123456')
        user.save()
        return user

    def tearDown(self) -> None:
        print('\nTeste finalizado')
        return super().tearDown()