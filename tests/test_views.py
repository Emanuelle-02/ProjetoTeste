from django.urls import reverse
from django.contrib.messages import get_messages
from .test_base import TestSetup

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
        self.assertEquals(response.status_code, 302)

    def test_deve_realizar_login_sem_problemas(self):
        user = self.create_test_user()
        response = self.client.post(reverse("login"), {
            'username': user.username,
            'password': '123456'
        })
        self.assertEquals(response.status_code, 302)

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
        self.assertEquals(response.status_code, 409)

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
        self.assertEquals(response.status_code, 409)

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
        self.assertEquals(response.status_code, 401)
        storage = get_messages(response.wsgi_request)
        self.assertIn("Informe um formato de email válido!",
                      list(map(lambda x: x.message, storage)))

    def test_nao_deve_logar_senha_invalida(self):
        user = self.create_test_user()
        response = self.client.post(reverse("login"), {
            'username': user.username,
            'password': '12345'
        })
        
        self.assertEquals(response.status_code, 401)
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
        self.assertEquals(response.status_code, 401)

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
        self.assertEquals(response.status_code, 401)

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
        self.assertEquals(response.status_code, 401)

        storage = get_messages(response.wsgi_request)
        self.assertIn("A senha deve possuir no mínimo 6 caracteres",
                      list(map(lambda x: x.message, storage)))