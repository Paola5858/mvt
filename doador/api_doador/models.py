from django.db import models

class TipoSanguineo(models.Model):
    tipo = models.CharField(max_length=3)
    
    def __str__(self):
        return self.tipo

class Doador(models.Model):
    nome = models.CharField(max_length=100)
    tipo_sanguineo = models.ForeignKey(TipoSanguineo, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome
