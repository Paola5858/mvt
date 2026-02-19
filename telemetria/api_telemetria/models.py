"""Models da API de Telemetria de Veículos."""
from django.db import models


class Marca(models.Model):
    """Marca do veículo."""
    nome = models.CharField(max_length=100, verbose_name="Nome da Marca")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Modelo(models.Model):
    """Modelo do veículo."""
    nome = models.CharField(max_length=100, verbose_name="Nome do Modelo")

    class Meta:
        verbose_name = "Modelo"
        verbose_name_plural = "Modelos"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    """Veículo cadastrado no sistema."""
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="veiculos")
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, related_name="veiculos")
    ano = models.IntegerField(verbose_name="Ano")
    horimetro = models.FloatField(verbose_name="Horímetro")

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ['id']

    def __str__(self):
        return f"{self.marca.nome} {self.modelo.nome} - {self.ano}"


class UnidadeMedida(models.Model):
    """Unidade de medida para as medições."""
    nome = models.CharField(max_length=50, verbose_name="Nome da Unidade")

    class Meta:
        verbose_name = "Unidade de Medida"
        verbose_name_plural = "Unidades de Medida"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Medicao(models.Model):
    """Tipo de medição realizada."""
    TIPO_CHOICES = [
        ('horimetro', 'Horímetro'),
        ('odometro', 'Odômetro'),
        ('combustivel', 'Combustível'),
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, verbose_name="Tipo")
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.CASCADE, related_name="medicoes")

    class Meta:
        verbose_name = "Medição"
        verbose_name_plural = "Medições"
        ordering = ['tipo']

    def __str__(self):
        return f"{self.get_tipo_display()} ({self.unidade_medida.nome})"


class MedicaoVeiculo(models.Model):
    """Registro de medição de um veículo."""
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name="medicoes")
    medicao = models.ForeignKey(Medicao, on_delete=models.CASCADE, related_name="registros")
    data = models.DateField(verbose_name="Data")
    valor = models.FloatField(verbose_name="Valor")

    class Meta:
        verbose_name = "Medição de Veículo"
        verbose_name_plural = "Medições de Veículos"
        ordering = ['-data']

    def __str__(self):
        return f"{self.veiculo} - {self.medicao.tipo} - {self.valor}"
