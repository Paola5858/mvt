from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import Talhao
from .serializers import TalhaoSerializer

class TalhaoViewSet(ModelViewSet):
    queryset = Talhao.objects.all()
    serializer_class = TalhaoSerializer
