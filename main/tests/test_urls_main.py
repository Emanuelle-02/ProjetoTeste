import datetime
from django.test import Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .test_base import TestSetup
import logging
from django.urls import reverse
from main.models import *
from usuario.models import User

logger = logging.getLogger('django.request')
logger.setLevel(logging.ERROR)
class TestUrlsMain(TestSetup):
    def test_dashboard(self):
        self.create_test_user()
        self.login()
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_minhas_despesas(self):
        self.create_test_user()
        self.login()
        response = self.client.get(reverse("minhas_despesas"))
        self.assertEqual(response.status_code, 200)
        
    def test_minha_renda(self):
        self.create_test_user()
        self.login()
        response = self.client.get(reverse("listagem_renda"))
        self.assertEqual(response.status_code, 200)

    def test_listar_categoria(self):
        self.create_test_user()
        self.login()
        response = self.client.get(reverse("listagem_categorias"))
        self.assertEqual(response.status_code, 200)

    def test_exibe_estatistica(self):
        self.create_test_user()
        self.login()
        response = self.client.get(reverse("estatistica"))
        self.assertEqual(response.status_code, 200)

    def test_exibe_estatistica_renda(self):
        self.create_test_user()
        self.login()
        response = self.client.get(reverse("estatistica_renda"))
        self.assertEqual(response.status_code, 200)
