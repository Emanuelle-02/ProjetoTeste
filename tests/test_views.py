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

class TestViews(TestSetup):
    def test_deve_exibir_pagina_cadastro(self):
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/cadastro.html")

    def test_deve_exibir_pagina_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")

    def test_deve_cadastrar_usuario(self):
        data = {
            "username": "outro",
            "email": "exemplo@gmail.com",   
            "password":"123456"
        }
        response = self.client.post(reverse("cadastro"), data)
        self.assertEqual(response.status_code, 302)

    def test_deve_realizar_login_sem_problemas(self):
        user = self.create_test_user()
        response = self.client.post(reverse("login"), {
            'username': user.username,
            'password': '123456'
        })
        self.assertEqual(response.status_code, 302)

        storage = get_messages(response.wsgi_request)

        self.assertIn(f'Olá, {user.username}',
                      list(map(lambda x: x.message, storage)))

    def test_nao_deve_cadastrar_username_ja_cadastrado(self):
        data = {
            "username": "outro",
            "email": "exemplo2@gmail.com",   
            "password":"123456"
        }
        self.client.post(reverse("cadastro"), data) # faz o request para cadastrar usuário com o mesmo username
        response = self.client.post(reverse("cadastro"), data) # faz outro request novamente, que deve falhar pq o usuário já existe
        self.assertEqual(response.status_code, 409)

        storage = get_messages(response.wsgi_request)
        self.assertIn('Esse nome de usuário já existe, escolha outro',
                      list(map(lambda x: x.message, storage)))

    def test_nao_deve_cadastrar_email_ja_cadastrado(self):
        data = {
            "username": "qualquerum",
            "email": "qualquerum@gmail.com",
            "password": "123456"
        }

        data_test = {
            "username": "qualquer",
            "email": "qualquerum@gmail.com",
            "password": "123456"
        }

        self.client.post(reverse("cadastro"), data) # O primeiro deve funcionar
        response = self.client.post(reverse("cadastro"), data_test) # o segundo deve falhar
        self.assertEqual(response.status_code, 409)

        storage = get_messages(response.wsgi_request)
        self.assertIn('Esse email já foi utilizado, escolha outro',
                      list(map(lambda x: x.message, storage)))

    def test_nao_deve_cadastrar_email_invalido(self):
        data = {
            "username": "usuario2",
            "email": "usuario!gmail.com",
            "password": "123456"
        }

        response = self.client.post(reverse("cadastro"), data)
        self.assertEqual(response.status_code, 401)
        storage = get_messages(response.wsgi_request)
        self.assertIn("Informe um formato de email válido!",
                      list(map(lambda x: x.message, storage)))

    def test_nao_deve_logar_senha_invalida(self):
        user = self.create_test_user()
        response = self.client.post(reverse("login"), {
            'username': user.username,
            'password': 'senha'
        })
        
        self.assertEqual(response.status_code, 401)
        storage = get_messages(response.wsgi_request)
        self.assertIn("Usuário ou senha inválida",
                      list(map(lambda x: x.message, storage)))

    def test_nao_deve_cadastrar_usuario_vazio(self):
        data = {
            "username": "",
            "email": "tantofaz@gmail.com",   
            "password":"123456"
        }
        response = self.client.post(reverse("cadastro"), data)
        self.assertEqual(response.status_code, 401)

        storage = get_messages(response.wsgi_request)
        self.assertIn("Informe um nome de usuário",
                      list(map(lambda x: x.message, storage)))

    def test_nao_deve_cadastrar_senha_com_menos_de_seis_caracteres(self):
        data = {
            "username": "outroqualquer",
            "email": "outroqualquer@gmail.com",   
            "password":"123"
        }
        response = self.client.post(reverse("cadastro"), data)
        self.assertEqual(response.status_code, 401)

        storage = get_messages(response.wsgi_request)
        self.assertIn("A senha deve possuir no mínimo 6 caracteres",
                      list(map(lambda x: x.message, storage)))

    def test_nao_deve_cadastrar_senha_vazia(self):
        data = {
            "username": "outroteste",
            "email": "outroteste@gmail.com",   
            "password":""
        }
        response = self.client.post(reverse("cadastro"), data)
        self.assertEqual(response.status_code, 401)

        storage = get_messages(response.wsgi_request)
        self.assertIn("A senha deve possuir no mínimo 6 caracteres",
                      list(map(lambda x: x.message, storage)))

        
    def test_logout_user(self):
        response = self.client.get(reverse("logout"), follow=True)
        self.assertEqual(response.status_code, 200)


    #----- TESTE APP MAIN ----- #
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