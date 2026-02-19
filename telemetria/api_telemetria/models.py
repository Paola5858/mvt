"""Models da API de Telemetria."""
from django.db import models


class Setor(models.Model):
    """
    Representa um setor físico onde sensores são instalados.
    
    Attributes:
        nome: Nome identificador do setor
        localizacao: Localização física ou descrição do setor
    """
    nome = models.CharField(max_length=100, verbose_name="Nome do Setor")
    localizacao = models.CharField(max_length=200, verbose_name="Localização")

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Sensor(models.Model):
    """
    Representa um sensor instalado em um setor.
    
    Attributes:
        setor: Referência ao setor onde o sensor está instalado
        tipo: Tipo do sensor (temperatura, umidade, etc.)
        status: Status operacional do sensor
    """
    setor = models.ForeignKey(
        Setor, 
        on_delete=models.CASCADE, 
        related_name="sensores",
        verbose_name="Setor"
    )
    tipo = models.CharField(max_length=100, verbose_name="Tipo de Sensor")
    status = models.CharField(max_length=50, verbose_name="Status")

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensores"
        ordering = ['id']

    def __str__(self):
        return f"{self.tipo} - {self.setor.nome}"


class Leitura(models.Model):
    """
    Representa uma leitura capturada por um sensor.
    
    Attributes:
        sensor: Referência ao sensor que realizou a leitura
        valor: Valor numérico da leitura
        data_hora: Timestamp automático da criação da leitura
    """
    sensor = models.ForeignKey(
        Sensor, 
        on_delete=models.CASCADE, 
        related_name="leituras",
        verbose_name="Sensor"
    )
    valor = models.FloatField(verbose_name="Valor da Leitura")
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora")

    class Meta:
        verbose_name = "Leitura"
        verbose_name_plural = "Leituras"
        ordering = ['-data_hora']
        indexes = [
            models.Index(fields=['-data_hora']),
            models.Index(fields=['sensor', '-data_hora']),
        ]

    def __str__(self):
        return f"{self.valor} - {self.sensor.tipo}"
