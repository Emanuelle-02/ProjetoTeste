from django.urls import path 
from . import views


urlpatterns = [
    path('login', views.login_usuario, name='login'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('logout', views.logout_user, name='logout'),

]