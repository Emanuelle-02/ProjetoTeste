from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=250)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Ganho(models.Model):
    descricao = models.TextField()
    valor = models.FloatField()
    data = models.DateField(default=now)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) 

class Despesas(models.Model):
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    valor = models.FloatField()
    data = models.DateField(default=now)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)