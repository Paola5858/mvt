from rest_framework import viewsets
from .models import TipoSanguineo, Doador
from .serializers import TipoSanguineoSerializer, DoadorSerializer

class TipoSanguineoViewSet(viewsets.ModelViewSet):
    queryset = TipoSanguineo.objects.all()
    serializer_class = TipoSanguineoSerializer

class DoadorViewSet(viewsets.ModelViewSet):
    queryset = Doador.objects.all()
    serializer_class = DoadorSerializer
