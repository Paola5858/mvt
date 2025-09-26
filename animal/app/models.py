from django.db import models

class Animal(models.Model):
    nome = models.CharField(max_length=100)
    tutor = models.CharField(max_length=100)
    idade = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nome
