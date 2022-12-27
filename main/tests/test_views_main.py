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

class TestViewsMain(TestSetup):
    def test_add_ganho(self):
        self.create_test_user()
        self.login()
        response_200 = self.client.post(reverse('add_renda'), data={
            "descricao": "Teste qualquer",
            "valor": 120,
            "data": datetime.date(2022, 12, 22)
        }, follow=True)
        self.assertEqual(response_200.status_code, 200)

    def test_add_categoria(self):
        self.create_test_user()
        self.login()
        response_200 = self.client.post(reverse('add_categoria'), data={
            "nome": "Teste qualquer"
        }, follow=True)
        self.assertEqual(response_200.status_code, 200)

    def setUp(self):
        user = User.objects.create(username="usuarioTeste", email="test")
        user.set_password("senha123")
        user.save()
        self.clientC = Client()
        self.client.login(username="usuarioTeste", password="senha123")
        self.categoriaC = Categoria.objects.create(nome="CategoriaTeste",user=user)
        self.despesa = Despesas.objects.create(
            id=1,
            descricao="Qualquer",
            valor=25,
            data=datetime.date(2022, 12, 23),
            categoria=self.categoriaC,
            user=user
            
            )

        self.ganho = Ganho.objects.create(
            id=1,
            descricao="Extra",
            valor=40,
            data=datetime.date(2022, 12, 23),
            user=user
            
            )

    def test_add_despesa(self):
        response = self.client.post(
            reverse("add_despesa"),
            {
                "descricao": "Seila",
                "data": datetime.date(2022, 12, 23),
                "valor": 50,
                "categoria": self.categoriaC,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_edit_ganho(self):
        response = self.client.post(
            reverse("editar_renda", kwargs={"id": 1}),
            {
                "descricao": "Extra2",
                "valor": 40,
                "data": datetime.date(2022, 12, 23),
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_remove_ganho(self):
        response = self.client.delete(
            reverse("delete_renda", kwargs={"id": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_remove_categoria(self):
        response = self.client.delete(
            reverse("delete_categoria", kwargs={"id": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_remove_despesa(self):
        response = self.client.delete(
            reverse("delete_despesa", kwargs={"id": 1}), follow=True
        )
        self.assertEqual(response.status_code, 200)