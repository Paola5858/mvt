from django.db import models

# Create your models here.
from django.db import models

class Talhao(models.Model):
    nome = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=6, decimal_places=2)
    cultura = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
