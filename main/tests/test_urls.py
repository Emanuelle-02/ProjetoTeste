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

class TestUrlsAuth(TestSetup):
    def test_deve_exibir_pagina_cadastro(self):
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/cadastro.html")

    def test_deve_exibir_pagina_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")