from django.shortcuts import render,redirect
from django.contrib import messages
from validate_email import validate_email
from . models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.
def cadastro(request):
    if request.method == "POST":
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if len(password)<6:
            messages.add_message(request,messages.ERROR, 'A senha deve possuir no mínimo 6 caracteres')
            context['has_error'] = True
            return render(request, 'auth/cadastro.html', context, status=401)

        if not validate_email(email):
            messages.add_message(request,messages.ERROR, 'Informe um formato de email válido!')
            context['has_error'] = True
            return render(request, 'auth/cadastro.html', context, status=401)

        if not username:
            messages.add_message(request,messages.ERROR, 'Informe um nome de usuário')
            context['has_error'] = True
            return render(request, 'auth/cadastro.html', context, status=401)

        if User.objects.filter(username=username).exists():
            messages.add_message(request,messages.ERROR, 'Esse nome de usuário já existe, escolha outro')
            context['has_error'] = True

            return render(request, 'auth/cadastro.html', context, status=409)

        if User.objects.filter(email=email).exists():
            messages.add_message(request,messages.ERROR, 'Esse email já foi utilizado, escolha outro')
            context['has_error'] = True
            return render(request, 'auth/cadastro.html', context, status=409)

        

        user=User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Conta criada com sucesso! Você já pode realizar o login')
        return redirect('login')

    return render(request, 'auth/cadastro.html')

def login_usuario(request):
    if request.method == 'POST':
        context={'data':request.POST}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha inválida')
            return render(request, 'auth/login.html', context, status=401)
        
        login(request, user)
        messages.add_message(request, messages.SUCCESS, f'Olá, {user.username}')
        return redirect(reverse('index'))

    return render(request, 'auth/login.html')

def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Você saiu da sua conta')
    return redirect(reverse('index'))