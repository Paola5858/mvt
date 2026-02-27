from django.db import models

class TipoSanguineo(models.Model):
    TIPOS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    tipo = models.CharField(max_length=3, choices=TIPOS, unique=True)
    
    class Meta:
        verbose_name = 'Tipo Sanguíneo'
        verbose_name_plural = 'Tipos Sanguíneos'
    
    def __str__(self):
        return self.tipo

class Doador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    tipo_sanguineo = models.ForeignKey(TipoSanguineo, on_delete=models.PROTECT, related_name='doadores')
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=15)
    ultima_doacao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Doador'
        verbose_name_plural = 'Doadores'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.nome} - {self.tipo_sanguineo}"
