from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from .models import (
    Marca,
    Modelo,
    Veiculo,
    UnidadeMedida,
    Medicao,
    MedicaoVeiculo,
    MedicaoVeiculoTemp,
    MedicaoVeiculoIoT,
)
from .serializers import (
    MarcaSerializer,
    ModeloSerializer,
    VeiculoSerializer,
    UnidadeMedidaSerializer,
    MedicaoSerializer,
    MedicaoVeiculoSerializer,
    UploadCSVSerializer,
    MedicaoVeiculoTempSerializer,
    SyncPayloadSerializer,
)
from .services import processar_csv_medicoes, SyncService


class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'id']
    ordering = ['nome']

    @swagger_auto_schema(
        operation_summary="Listar marcas",
        operation_description="Lista todas as marcas cadastradas",
        responses={200: MarcaSerializer(many=True)},
        tags=['Marcas']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Criar marca",
        operation_description="Cadastra uma nova marca",
        responses={201: MarcaSerializer()},
        tags=['Marcas']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Detalhar marca",
        operation_description="Retorna uma marca conforme o ID informado",
        responses={200: MarcaSerializer()},
        tags=['Marcas']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar marca",
        operation_description="Atualiza dados de uma marca conforme o ID informado",
        responses={200: MarcaSerializer()},
        tags=['Marcas']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar marca parcialmente",
        operation_description="Atualiza parcialmente os dados de uma marca conforme o ID informado",
        responses={200: MarcaSerializer()},
        tags=['Marcas']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Remover marca",
        operation_description="Remove uma marca conforme o ID informado",
        responses={204: "Marca removida com sucesso"},
        tags=['Marcas']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'id']
    ordering = ['nome']

    @swagger_auto_schema(
        operation_summary="Listar modelos",
        operation_description="Lista todos os modelos cadastrados",
        responses={200: ModeloSerializer(many=True)},
        tags=['Modelos']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Criar modelo",
        operation_description="Cadastra um novo modelo",
        responses={201: ModeloSerializer()},
        tags=['Modelos']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Detalhar modelo",
        operation_description="Retorna um modelo conforme o ID informado",
        responses={200: ModeloSerializer()},
        tags=['Modelos']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar modelo",
        operation_description="Atualiza dados de um modelo conforme o ID informado",
        responses={200: ModeloSerializer()},
        tags=['Modelos']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar modelo parcialmente",
        operation_description="Atualiza parcialmente os dados de um modelo conforme o ID informado",
        responses={200: ModeloSerializer()},
        tags=['Modelos']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Remover modelo",
        operation_description="Remove um modelo conforme o ID informado",
        responses={204: "Modelo removido com sucesso"},
        tags=['Modelos']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.select_related('marca', 'modelo').all()
    serializer_class = VeiculoSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['marca', 'modelo', 'ano']
    search_fields = ['descricao', 'marca__nome', 'modelo__nome']
    ordering_fields = ['ano', 'horimetro', 'id']
    ordering = ['-ano']

    @swagger_auto_schema(
        operation_summary="Listar veículos",
        operation_description="Lista todos os veículos cadastrados",
        responses={200: VeiculoSerializer(many=True)},
        tags=['Veículos']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Criar veículo",
        operation_description="Cadastra um novo veículo com marca, modelo, ano e horímetro",
        responses={201: VeiculoSerializer()},
        tags=['Veículos']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Detalhar veículo",
        operation_description="Retorna um veículo conforme o ID informado",
        responses={200: VeiculoSerializer()},
        tags=['Veículos']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar veículo",
        operation_description="Atualiza dados de um veículo conforme o ID informado",
        responses={200: VeiculoSerializer()},
        tags=['Veículos']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar veículo parcialmente",
        operation_description="Atualiza parcialmente os dados de um veículo conforme o ID informado",
        responses={200: VeiculoSerializer()},
        tags=['Veículos']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Remover veículo",
        operation_description="Remove um veículo conforme o ID informado",
        responses={204: "Veículo removido com sucesso"},
        tags=['Veículos']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get"], url_path="medicoes")
    @swagger_auto_schema(
        operation_summary="Listar medições de um veículo",
        operation_description="Retorna todas as medições registradas para um veículo específico",
        responses={200: MedicaoVeiculoSerializer(many=True)},
        tags=["Veículos"],
    )
    def medicoes_por_veiculo(self, request, pk=None):
        veiculo = get_object_or_404(Veiculo, pk=pk)
        medicoes = (
            MedicaoVeiculo.objects.filter(veiculo=veiculo)
            .select_related("medicao", "medicao__unidade_medida")
            .order_by("-data")
        )
        serializer = MedicaoVeiculoSerializer(medicoes, many=True)
        return Response(serializer.data)


class UnidadeMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadeMedida.objects.all()
    serializer_class = UnidadeMedidaSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    @swagger_auto_schema(
        operation_summary="Listar unidades de medida",
        operation_description="Lista todas as unidades de medida cadastradas",
        responses={200: UnidadeMedidaSerializer(many=True)},
        tags=['Unidades de Medida']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Criar unidade de medida",
        operation_description="Cadastra uma nova unidade de medida",
        responses={201: UnidadeMedidaSerializer()},
        tags=['Unidades de Medida']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Detalhar unidade de medida",
        operation_description="Retorna uma unidade de medida conforme o ID informado",
        responses={200: UnidadeMedidaSerializer()},
        tags=['Unidades de Medida']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar unidade de medida",
        operation_description="Atualiza dados de uma unidade de medida conforme o ID informado",
        responses={200: UnidadeMedidaSerializer()},
        tags=['Unidades de Medida']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar unidade de medida parcialmente",
        operation_description="Atualiza parcialmente os dados de uma unidade de medida conforme o ID informado",
        responses={200: UnidadeMedidaSerializer()},
        tags=['Unidades de Medida']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Remover unidade de medida",
        operation_description="Remove uma unidade de medida conforme o ID informado",
        responses={204: "Unidade de medida removida com sucesso"},
        tags=['Unidades de Medida']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MedicaoViewSet(viewsets.ModelViewSet):
    queryset = Medicao.objects.select_related('unidade_medida').all()
    serializer_class = MedicaoSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tipo', 'unidade_medida']
    search_fields = ['tipo']

    @swagger_auto_schema(
        operation_summary="Listar medições",
        operation_description="Lista todas as medições cadastradas",
        responses={200: MedicaoSerializer(many=True)},
        tags=['Medições']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Criar medição",
        operation_description="Cadastra uma nova medição com tipo e unidade de medida",
        responses={201: MedicaoSerializer()},
        tags=['Medições']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Detalhar medição",
        operation_description="Retorna uma medição conforme o ID informado",
        responses={200: MedicaoSerializer()},
        tags=['Medições']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar medição",
        operation_description="Atualiza dados de uma medição conforme o ID informado",
        responses={200: MedicaoSerializer()},
        tags=['Medições']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar medição parcialmente",
        operation_description="Atualiza parcialmente os dados de uma medição conforme o ID informado",
        responses={200: MedicaoSerializer()},
        tags=['Medições']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Remover medição",
        operation_description="Remove uma medição conforme o ID informado",
        responses={204: "Medição removida com sucesso"},
        tags=['Medições']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MedicaoVeiculoViewSet(viewsets.ModelViewSet):
    queryset = MedicaoVeiculo.objects.select_related('veiculo', 'medicao').all()
    serializer_class = MedicaoVeiculoSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['veiculo', 'medicao', 'data']
    search_fields = ['veiculo__descricao']
    ordering_fields = ['data', 'valor']
    ordering = ['-data']

    @swagger_auto_schema(
        operation_summary="Listar medições de veículos",
        operation_description="Lista todos os registros de medição de veículos",
        responses={200: MedicaoVeiculoSerializer(many=True)},
        tags=['Medições de Veículos']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Criar medição de veículo",
        operation_description="Registra uma nova medição para um veículo",
        responses={201: MedicaoVeiculoSerializer()},
        tags=['Medições de Veículos']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Detalhar medição de veículo",
        operation_description="Retorna um registro de medição conforme o ID informado",
        responses={200: MedicaoVeiculoSerializer()},
        tags=['Medições de Veículos']
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar medição de veículo",
        operation_description="Atualiza um registro de medição conforme o ID informado",
        responses={200: MedicaoVeiculoSerializer()},
        tags=['Medições de Veículos']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Atualizar medição de veículo parcialmente",
        operation_description="Atualiza parcialmente um registro de medição conforme o ID informado",
        responses={200: MedicaoVeiculoSerializer()},
        tags=['Medições de Veículos']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Remover medição de veículo",
        operation_description="Remove um registro de medição conforme o ID informado",
        responses={204: "Registro removido com sucesso"},
        tags=['Medições de Veículos']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ImportarMedicaoCSVViewSet(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Importar medições via CSV",
        operation_description="Recebe um arquivo .csv com colunas: veiculoid, medicaoid, data, valor. Salva os dados na tabela temporária.",
        tags=["Importação CSV"]
    )
    def post(self, request, *args, **kwargs):
        serializer = UploadCSVSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        arquivo = validated.get("arquivo")
        if not arquivo:
            return Response(
                {"erro": "Arquivo não fornecido"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            resultado = processar_csv_medicoes(arquivo)
            return Response(
                {"mensagem": "Arquivo processado com sucesso.", **resultado},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"erro": "Falha ao processar o arquivo.", "detalhe": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MedicaoVeiculoTempViewSet(viewsets.ModelViewSet):
    serializer_class = MedicaoVeiculoTempSerializer
    queryset = MedicaoVeiculoTemp.objects.all()

    @swagger_auto_schema(
        operation_description="Retorna todas as informações de medições dos arquivos importados",
        responses={200: MedicaoVeiculoTempSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SyncOfflineView(APIView):
    """
    View burra, do jeito que tem que ser.
    Recebe o JSON do ESP32, passa pro serializer validar e chama o service.

    POST /api/sync/offline/
    {
        "veiculo_id": 123,
        "medicoes": [
            {
                "id_veiculo": 123,
                "temperatura": 85.5,
                "vibracao": 3.2,
                "rpm": 2500,
                "timestamp_coleta": "2026-04-16T10:30:00Z"
            }
        ]
    }
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Sincronizar medições offline do ESP32",
        operation_description="Recebe batch de medições offline e insere no banco atômicamente.",
        request_body=SyncPayloadSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "registros_inseridos": {"type": "integer"},
                    "registros_processados": {"type": "integer"},
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "erro": {"type": "string"},
                    "detalhes": {"type": "object"},
                },
            },
        },
        tags=["Sincronização Offline"],
    )
    def post(self, request):
        serializer = SyncPayloadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"erro": "Payload sujo", "detalhes": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        dados_validados = serializer.validated_data

        veiculo_id = dados_validados.get("veiculo_id")
        medicoes_data = dados_validados.get("medicoes")

        if veiculo_id is None or medicoes_data is None:
            return Response(
                {"erro": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST
            )

        resultado = SyncService.processar_sync_offline(
            veiculo_id=veiculo_id,
            medicoes_data=medicoes_data,
        )

        # Se status é sucesso, retorna 201. Se erro, retorna 400.
        response_status = (
            status.HTTP_201_CREATED
            if resultado["status"] == "sucesso"
            else status.HTTP_400_BAD_REQUEST
        )

        return Response(resultado, status=response_status)
