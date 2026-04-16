"""Serializers da API de Telemetria de Veículos."""
from rest_framework import serializers
from .models import Marca, Modelo, Veiculo, UnidadeMedida, Medicao, MedicaoVeiculo, MedicaoVeiculoTemp


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nome']
        extra_kwargs = {
            'id': {'help_text': 'Identificador único da marca'},
            'nome': {'help_text': 'Nome da marca do veículo (ex: FIAT, VOLKSWAGEN)'},
        }

    def validate_nome(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("O nome da marca não pode ser vazio.")
        if len(value) < 2:
            raise serializers.ValidationError(
                "O nome da marca deve ter pelo menos 2 caracteres."
            )
        return value.strip().upper()


class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = ["id", "nome"]
        extra_kwargs = {
            "id": {"help_text": "Identificador único do modelo"},
            "nome": {"help_text": "Nome do modelo do veículo (ex: UNO, GOL, CIVIC)"},
        }

    def validate_nome(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("O nome do modelo não pode ser vazio.")
        if len(value) < 2:
            raise serializers.ValidationError("O nome do modelo deve ter pelo menos 2 caracteres.")
        return value.strip().upper()


class VeiculoSerializer(serializers.ModelSerializer):
    marca_nome = serializers.CharField(source='marca.nome', read_only=True)
    modelo_nome = serializers.CharField(source='modelo.nome', read_only=True)

    class Meta:
        model = Veiculo
        fields = [
            "id",
            "descricao",
            "marca",
            "marca_nome",
            "modelo",
            "modelo_nome",
            "ano",
            "horimetro",
        ]
        extra_kwargs = {
            "id": {"help_text": "Identificador único do veículo"},
            "descricao": {
                "help_text": "Descrição do veículo (ex: Caminhão de entrega)"
            },
            "marca": {"help_text": "ID da marca do veículo"},
            "modelo": {"help_text": "ID do modelo do veículo"},
            "ano": {"help_text": "Ano de fabricação do veículo (entre 1900 e 2030)"},
            "horimetro": {"help_text": "Leitura atual do horímetro em horas"},
        }

    def validate_ano(self, value):
        if value < 1900 or value > 2030:
            raise serializers.ValidationError("O ano deve estar entre 1900 e 2030.")
        return value

    def validate_horimetro(self, value):
        if value < 0:
            raise serializers.ValidationError("O horímetro não pode ser negativo.")
        if value > 999999:
            raise serializers.ValidationError("O horímetro não pode exceder 999999.")
        return value

    def validate_descricao(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("A descrição não pode ser vazia.")
        return value.strip()


class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeMedida
        fields = ['id', 'nome']
        extra_kwargs = {
            'id': {'help_text': 'Identificador único da unidade de medida'},
            'nome': {'help_text': 'Nome da unidade de medida (ex: Horas, Quilômetros, Litros)'},
        }

    def validate_nome(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("O nome da unidade não pode ser vazio.")
        return value.strip()


class MedicaoSerializer(serializers.ModelSerializer):
    unidade_nome = serializers.CharField(source="unidade_medida.nome", read_only=True)

    class Meta:
        model = Medicao
        fields = ['id', 'tipo', 'unidade_medida', 'unidade_nome']
        extra_kwargs = {
            'id': {'help_text': 'Identificador único da medição'},
            'tipo': {'help_text': 'Tipo da medição: horimetro, odometro ou combustivel'},
            'unidade_medida': {'help_text': 'ID da unidade de medida utilizada'},
        }


class MedicaoVeiculoSerializer(serializers.ModelSerializer):
    veiculo_descricao = serializers.CharField(source='veiculo.descricao', read_only=True)
    medicao_tipo = serializers.CharField(source='medicao.tipo', read_only=True)

    class Meta:
        model = MedicaoVeiculo
        fields = [
            "id",
            "veiculo",
            "veiculo_descricao",
            "medicao",
            "medicao_tipo",
            "data",
            "valor",
        ]
        extra_kwargs = {
            "id": {"help_text": "Identificador único do registro"},
            "veiculo": {"help_text": "ID do veículo medido"},
            "medicao": {"help_text": "ID do tipo de medição realizada"},
            "data": {"help_text": "Data da medição no formato AAAA-MM-DD"},
            "valor": {"help_text": "Valor registrado na medição"},
        }

    def validate_valor(self, value):
        if value < 0:
            raise serializers.ValidationError("O valor não pode ser negativo.")
        if value > 9999999:
            raise serializers.ValidationError("O valor não pode exceder 9999999.")
        return value


class UploadCSVSerializer(serializers.Serializer):
    arquivo = serializers.FileField()

    def validate_arquivo(self, value):
        if not value.name.lower().endswith(".csv"):
            raise serializers.ValidationError("O arquivo enviado deve ser .csv")
        return value


class MedicaoVeiculoTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicaoVeiculoTemp
        fields = "__all__"


class MedicaoTelemetriaSerializer(serializers.Serializer):
    """
    Serializer blindado para dados de IoT do ESP32.
    Sensor mente, a gente não confia em input externo.
    """

    id_veiculo = serializers.IntegerField(required=True)
    temperatura = serializers.FloatField(required=True)
    vibracao = serializers.FloatField(required=True)
    rpm = serializers.IntegerField(required=True)
    timestamp_coleta = serializers.DateTimeField(required=True)

    def validate_temperatura(self, value):
        if value < -50 or value > 250:
            raise serializers.ValidationError(
                "Temperatura fora da realidade operacional. Limite: -50°C a 250°C. "
                f"Recebido: {value}°C"
            )
        return value

    def validate_vibracao(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError(
                f"Vibração inválida. Limite: 0 a 100 mm/s. Recebido: {value} mm/s"
            )
        return value

    def validate_rpm(self, value):
        if value < 0 or value > 10000:
            raise serializers.ValidationError(
                "RPM inválido. Motor explodiu ou sensor pifou. Limite: 0 a 10000 RPM. "
                f"Recebido: {value} RPM"
            )
        return value

    def validate_id_veiculo(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                f"ID do veículo inválido: {value}. Deve ser positivo."
            )
        return value


class SyncPayloadSerializer(serializers.Serializer):
    """
    Valida o payload inteiro de sync offline.
    """

    veiculo_id = serializers.IntegerField(required=True)
    medicoes = MedicaoTelemetriaSerializer(many=True, required=True)

    def validate_veiculo_id(self, value):
        if value <= 0:
            raise serializers.ValidationError(f"ID do veículo inválido: {value}")
        # Validação rápida no nível do serializer
        if not Veiculo.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                f"Veículo {value} não cadastrado na frota."
            )
        return value

    def validate_medicoes(self, value):
        if not value:
            raise serializers.ValidationError(
                "Payload sem medições. Envie pelo menos uma medição."
            )
        if len(value) > 10000:
            raise serializers.ValidationError(
                f"Payload gigante: {len(value)} medições. Máximo: 10000. "
                "Quebra em múltiplos requests."
            )
        return value
